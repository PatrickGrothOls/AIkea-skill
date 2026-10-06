/** Scope: Prepare an unpublished anonymous intake form and its private submission trigger. */
class ReportingSetup {
  prepare() {
    const props = PropertiesService.getScriptProperties();
    if (props.getProperty('FORM_ID')) throw new Error('Form already configured; do not create a duplicate.');
    const form = FormApp.create('AIkea problem report', false);
    form.setAcceptingResponses(false).setCollectEmail(false).setLimitOneResponsePerUser(false)
      .setAllowResponseEdits(false).setPublishingSummary(false).setShowLinkToRespondAgain(false)
      .setDescription('Review the report prepared in your chat. Approved reports are sent to ' +
        'AIkea and published on its public issue tracker. Do not include names, email addresses, ' +
        'home details, credentials or private files. Google stores this form response.')
      .setConfirmationMessage('Your report has been received. Publication may be delayed or held ' +
        'for review. This receipt does not confirm that a public issue has been created.');
    const report = form.addParagraphTextItem().setTitle('Report').setRequired(true)
      .setValidation(FormApp.createParagraphTextValidation().requireTextLengthLessThanOrEqualTo(6000).build());
    const consent = form.addCheckboxItem().setTitle('Public publication').setRequired(true)
      .setChoiceValues([ReportPolicy.consent]);
    const template = form.createResponse().withItemResponse(report.createResponse('AIKEA_REPORT')).toPrefilledUrl();
    props.setProperties({ FORM_ID: form.getId(), REPORT_ITEM_ID: String(report.getId()),
      CONSENT_ITEM_ID: String(consent.getId()), PREFILL_TEMPLATE: template, ENABLED: 'false' });
    ScriptApp.newTrigger('receiveIssueReport').forForm(form).onFormSubmit().create();
    console.log('Prepared unpublished form: ' + form.getEditUrl());
    console.log('Keep intake disabled until the operator activation checklist is complete.');
  }

  configuration() {
    const props = PropertiesService.getScriptProperties();
    const form = FormApp.openById(props.getProperty('FORM_ID'));
    if (props.getProperty('ENABLED') !== 'true' || !props.getProperty('GITHUB_TOKEN') ||
        !form.isPublished() || !form.isAcceptingResponses() || form.collectsEmail() ||
        form.hasLimitOneResponsePerUser() || form.isPublishingSummary()) {
      throw new Error('Complete and verify the operator activation checklist first.');
    }
    console.log(JSON.stringify({ status: 'ready',
      prefill_url_template: props.getProperty('PREFILL_TEMPLATE') }, null, 2));
  }
}

// Apps Script's Run menu needs a top-level wrapper; setup logic belongs to the class.
function prepareReportingForm() {
  new ReportingSetup().prepare();
}

// Export only public form configuration, never the token or private receipt state.
function exportReportingConfiguration() {
  new ReportingSetup().configuration();
}
