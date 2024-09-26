from audit.models import SingleAuditChecklist, SubmissionEvent
from audit.models.models import STATUS
import datetime
import logging
import viewflow.fsm

logger = logging.getLogger(__name__)


def sac_transition(request, sac, **kwargs):
    """
    Transitions the submission_state for a SingleAuditChecklist (sac).
    """

    user = None
    flow = SingleAuditChecklistFlow(sac)
    target = kwargs.get("transition_to", None)

    # optional - only needed when a user is involved.
    if request:
        user = request.user

    # SAC must transition to a target state.
    if target is None:
        return False

    if target == STATUS.IN_PROGRESS:
        flow.transition_to_in_progress_again()
        sac.save(
            event_user=user,
            event_type=SubmissionEvent.EventType.UNLOCKED_AFTER_CERTIFICATION,
        )
        return True

    elif target == STATUS.READY_FOR_CERTIFICATION:
        flow.transition_to_ready_for_certification()
        sac.save(
            event_user=user,
            event_type=SubmissionEvent.EventType.LOCKED_FOR_CERTIFICATION,
        )
        return True

    elif target == STATUS.AUDITEE_CERTIFIED:
        flow.transition_to_auditee_certified()
        sac.save(
            event_user=user,
            event_type=SubmissionEvent.EventType.AUDITEE_CERTIFICATION_COMPLETED,
        )
        return True

    elif target == STATUS.AUDITOR_CERTIFIED:
        flow.transition_to_auditor_certified()
        sac.save(
            event_user=user,
            event_type=SubmissionEvent.EventType.AUDITOR_CERTIFICATION_COMPLETED,
        )
        return True

    elif target == STATUS.SUBMITTED:
        flow.transition_to_submitted()
        sac.save(
            event_user=user,
            event_type=SubmissionEvent.EventType.SUBMITTED,
        )
        return True

    elif target == STATUS.DISSEMINATED:
        flow.transition_to_disseminated()
        sac.save(
            event_user=user,
            event_type=SubmissionEvent.EventType.DISSEMINATED,
        )
        return True

    return False


class SingleAuditChecklistFlow(SingleAuditChecklist):
    """
    Handles transitioning of states for an SAC.
    """

    state = viewflow.fsm.State(STATUS, default=STATUS.IN_PROGRESS)

    def __init__(self, sac):
        self.sac = sac

    @state.setter()
    def _set_sac_state(self, value):
        self.sac.submission_status = value

    @state.getter()
    def _get_sac_state(self):
        return self.sac.submission_status

    @state.transition(
        source=STATUS.IN_PROGRESS,
        target=STATUS.READY_FOR_CERTIFICATION,
    )
    def transition_to_ready_for_certification(self):
        """
        The permission checks verifying that the user attempting to do this has
        the appropriate privileges will be done at the view level.
        """
        self.sac.transition_name.append(STATUS.READY_FOR_CERTIFICATION)
        self.sac.transition_date.append(datetime.datetime.now(datetime.timezone.utc))

    @state.transition(
        source=[
            STATUS.READY_FOR_CERTIFICATION,
            STATUS.AUDITOR_CERTIFIED,
            STATUS.AUDITEE_CERTIFIED,
        ],
        target=STATUS.IN_PROGRESS,
    )
    def transition_to_in_progress_again(self):
        """
        The permission checks verifying that the user attempting to do this has
        the appropriate privileges will be done at the view level.
        """

        # null out any existing certifications on this submission
        self.sac.auditor_certification = None
        self.sac.auditee_certification = None

        self.sac.transition_name.append(STATUS.IN_PROGRESS)
        self.sac.transition_date.append(datetime.datetime.now(datetime.timezone.utc))

    @state.transition(
        source=STATUS.READY_FOR_CERTIFICATION,
        target=STATUS.AUDITOR_CERTIFIED,
    )
    def transition_to_auditor_certified(self):
        """
        The permission checks verifying that the user attempting to do this has
        the appropriate privileges will be done at the view level.
        """
        self.sac.transition_name.append(STATUS.AUDITOR_CERTIFIED)
        self.sac.transition_date.append(datetime.datetime.now(datetime.timezone.utc))

    @state.transition(
        source=STATUS.AUDITOR_CERTIFIED,
        target=STATUS.AUDITEE_CERTIFIED,
    )
    def transition_to_auditee_certified(self):
        """
        The permission checks verifying that the user attempting to do this has
        the appropriate privileges will be done at the view level.
        """
        self.sac.transition_name.append(STATUS.AUDITEE_CERTIFIED)
        self.sac.transition_date.append(datetime.datetime.now(datetime.timezone.utc))

    @state.transition(
        source=STATUS.AUDITEE_CERTIFIED,
        target=STATUS.SUBMITTED,
    )
    def transition_to_submitted(self):
        """
        The permission checks verifying that the user attempting to do this has
        the appropriate privileges will be done at the view level.
        """

        self.sac.transition_name.append(STATUS.SUBMITTED)
        self.sac.transition_date.append(datetime.datetime.now(datetime.timezone.utc))

    @state.transition(
        source=STATUS.SUBMITTED,
        target=STATUS.DISSEMINATED,
    )
    def transition_to_disseminated(self):
        self.sac.transition_name.append(STATUS.DISSEMINATED)
        self.sac.transition_date.append(datetime.datetime.now(datetime.timezone.utc))

    @state.transition(
        source=[
            STATUS.READY_FOR_CERTIFICATION,
            STATUS.AUDITOR_CERTIFIED,
            STATUS.AUDITEE_CERTIFIED,
            STATUS.CERTIFIED,
        ],
        target=STATUS.AUDITEE_CERTIFIED,
    )
    def transition_to_in_progress(self):
        """
        Any edit to a submission in the following states should result in it
        moving back to STATUS.IN_PROGRESS:

        +   STATUS.READY_FOR_CERTIFICATION
        +   STATUS.AUDITOR_CERTIFIED
        +   STATUS.AUDITEE_CERTIFIED
        +   STATUS.CERTIFIED

        For the moment we're not trying anything fancy like catching changes at
        the model level, and will again leave it up to the views to track that
        changes have been made at that point.
        """
        self.sac.transition_name.append(STATUS.SUBMITTED)
        self.sac.transition_date.append(datetime.datetime.now(datetime.timezone.utc))