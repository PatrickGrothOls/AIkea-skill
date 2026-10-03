/** Scope: Describe CNC delivery independently from unimplemented trade enquiries. */

import { Component } from "react";

export class QuoteDeliveryStatus extends Component {
  render() {
    const { delivery, receipt, error, sending, selected } = this.props;
    return (
      <div aria-live="polite" id="quote-availability" className="quote-availability">
        {receipt ? <p>CNC request sent to Patrick. Reference: <strong>{receipt.request_id}</strong>.</p>
          : <p>{sending ? (delivery.sign_in_required
            ? "Complete sign-in in your browser. Your source package will then upload."
            : "Uploading your source repository…")
            : delivery.enabled ? "Your editable source code, preview and preferences go directly to Patrick for a CNC quote. No STEP files or payment."
              : "CNC delivery has not been configured for this design yet."}</p>}
        {(selected.painting || selected.installation) &&
          <p>Painting and installation preferences are recorded, but no local tradespeople have been contacted.</p>}
        {error && <p role="alert">{error}</p>}
      </div>
    );
  }
}
