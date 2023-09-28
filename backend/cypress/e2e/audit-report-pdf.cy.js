import 'cypress-file-upload';
import { testCrossValidation } from '../support/cross-validation.js';
import { testLoginGovLogin } from '../support/login-gov.js';
//import { testLogoutGov } from '../support/logout-gov.js';
import { testValidAccess } from '../support/check-access.js';
import { testValidEligibility } from '../support/check-eligibility.js';
import { testValidAuditeeInfo } from '../support/auditee-info.js';
import { testValidGeneralInfo } from '../support/general-info.js';
import { testPdfAuditReport   } from '../support/report-pdf.js';

import {
  testWorkbookFederalAwards,
} from '../support/workbook-uploads.js';

const LOGIN_TEST_EMAIL_AUDITEE = Cypress.env('LOGIN_TEST_EMAIL_AUDITEE');
const LOGIN_TEST_PASSWORD_AUDITEE = Cypress.env('LOGIN_TEST_PASSWORD_AUDITEE');
const LOGIN_TEST_OTP_SECRET_AUDITEE = Cypress.env('LOGIN_TEST_OTP_SECRET_AUDITEE');

describe('Audit report PDF page', () => {
  before(() => {
    cy.session('login-session', () => {
      cy.visit('/');
      cy.login();
    });
  });

  it('Audit report PDF uploads successfully', () => {
    cy.visit('/');

    cy.url().should('include', '/');

    cy.get('label[for=check-start-new-submission]').click();

    cy.get('.usa-button').contains('Accept and start').click();

    cy.url().should('match', /\/report_submission\/eligibility\/$/);

    testValidEligibility();

    testValidAuditeeInfo();

    testValidAccess();

    testValidGeneralInfo();

    cy.get(".usa-link").contains("Federal Awards").click();
    testWorkbookFederalAwards(false);

    cy.get(".usa-link").contains("Audit report PDF").click();
    testPdfAuditReport(false);
  });

    it('Displays message if file has already been uploaded', () => {
      cy.visit(`/audit/`);
      cy.url().should('match', /\/audit\//);
      cy.get(':nth-child(4) > .usa-table > tbody > tr').last().find('td:nth-child(1)>.usa-link').click();
      cy.get('.usa-link').contains('Edit the Audit report PDF').click();
      cy.get('#already-submitted')
        .invoke('text')
        .then((text) => {
          const expectedText = 'A file has already been uploaded for this section. A successful reupload will overwrite your previous submission.';
          expect(text.trim()).to.equal(expectedText);
        });
    });

  });