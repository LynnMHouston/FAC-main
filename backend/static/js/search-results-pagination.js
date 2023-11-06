var FORM = document.getElementById('search-form');
const pagination_links = document.querySelectorAll('[aria-label^="Page"]');
const next_page_link = document.querySelectorAll('[aria-label="Next page"]');
const previous_page_link = document.querySelectorAll(
  '[aria-label="Previous page"]'
);

function attachEventHandlers() {
  // If any pagination links are clicked, set the page form element and submit it for a reload
  pagination_links.forEach((link) => {
    link.addEventListener('click', (e) => {
      e.preventDefault();
      FORM.elements['page'].value = link.textContent;
      FORM.submit();
    });
  });

  // If the next or previous page buttons are clicked, set the page form element to be +/- 1 and submit for a reload
  if (next_page_link[0]) {
    next_page_link[0].addEventListener('click', (e) => {
      e.preventDefault();
      FORM.elements['page'].value = parseInt(FORM.elements['page'].value) + 1;
      FORM.submit();
    });
  }
  if (previous_page_link[0]) {
    previous_page_link[0].addEventListener('click', (e) => {
      e.preventDefault();
      FORM.elements['page'].value = parseInt(FORM.elements['page'].value) - 1;
      FORM.submit();
    });
  }

  // The form resets to the default value, which is whatever the user entered on the last form submission, _not_ fully empty fields.
  // We cannot just loop over every form element, because buttons and hidden inputs should be handled differently.
  FORM.addEventListener('reset', (e) => {
    e.preventDefault();
    // Empty out textareas
    var text_areas = document.getElementsByTagName('textarea');
    Array.from(text_areas).forEach((input) => {
      input.value = '';
    });
    // Uncheck checkboxes
    var checkboxes = document.querySelectorAll('[type="checkbox"]');
    Array.from(checkboxes).forEach((checkbox) => {
      checkbox.checked = false;
    });
    // Wipe FAC release dates
    var start_date = document.getElementById('start-date');
    var end_date = document.getElementById('end-date');
    start_date.value = '';
    end_date.value = '';
    // Reset Cog/Over dropdown
    var default_option = document.getElementById('cog_or_oversight--none');
    default_option.selected = true;
    // Wipe agency name
    var agency_name = document.getElementById('agency-name');
    agency_name.value = '';

    FORM.reset();
  });
}

function init() {
  attachEventHandlers();
}

window.onload = init;
