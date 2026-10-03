/** Scope: Own quote preferences and one retryable CNC submission. */

import { Component } from "react";
import { QuoteServiceChoices } from "./QuoteServiceChoices";
import { QuoteRequestClient } from "./QuoteRequestClient";
import { QuoteDeliveryStatus } from "./QuoteDeliveryStatus";

export class QuoteRequestForm extends Component {
  client = new QuoteRequestClient();
  pendingRequest = null;
  state = {
    selected: { machining: true, painting: true, installation: true },
    finish: "discuss", colour: "", postcode: "", timing: "flexible", notes: "",
    delivery: { enabled: false }, receipt: null, sending: false, started: false, error: "",
  };

  async componentDidMount() {
    try {
      const delivery = await this.client.status();
      this.setState({ delivery, receipt: delivery.receipt || null });
    } catch (error) {
      this.setState({ error: error.message });
    }
  }

  changeField = (event) => {
    this.setState({ [event.target.name]: event.target.value });
  };

  toggleService = (id) => {
    this.setState(({ selected }) => ({ selected: { ...selected, [id]: !selected[id] } }));
  };

  submit = async (event) => {
    event.preventDefault();
    if (this.state.sending || this.state.receipt || !this.state.delivery.enabled) return;
    const { selected, finish, colour, postcode, timing, notes, delivery } = this.state;
    this.pendingRequest ||= { selected, finish, colour, postcode, timing, notes,
      preview: this.props.preview, title: this.props.title };
    this.setState({ sending: true, started: true, error: "" });
    try {
      const receipt = await this.client.submit(delivery.token, this.pendingRequest);
      this.setState({ receipt, sending: false });
    } catch (error) {
      this.setState({ sending: false, error: error.message });
    }
  };

  render() {
    const { selected, finish, colour, postcode, timing, notes, delivery, receipt, sending, started, error } = this.state;
    const hasService = Object.values(selected).some(Boolean);
    return (
      <form className="quote-form" onSubmit={this.submit}>
        <fieldset style={{ border: 0, padding: 0, margin: 0, minWidth: 0 }} disabled={started || Boolean(receipt)}>
        <QuoteServiceChoices selected={selected} finish={finish} colour={colour}
          onToggle={this.toggleService} onChange={this.changeField} />
        {!hasService && <p className="quote-hint" role="status">Choose at least one service for your quote.</p>}
        <div className="quote-logistics">
          <label>Postcode
            <input name="postcode" autoComplete="postal-code" value={postcode}
              placeholder="Enter postcode" maxLength={20} onChange={this.changeField} />
          </label>
          <label>Preferred timing
            <select name="timing" value={timing} onChange={this.changeField}>
              <option value="flexible">I'm flexible</option>
              <option value="soon">As soon as possible</option>
              <option value="1-3-months">In 1–3 months</option>
              <option value="later">Later this year</option>
            </select>
          </label>
        </div>
        <details className="quote-notes">
          <summary>Add a note or access details <span aria-hidden="true">+</span></summary>
          <label>Notes for your quote
            <textarea name="notes" value={notes} rows={3} maxLength={2000}
              placeholder="For example, stairs or access to your home" onChange={this.changeField} />
          </label>
        </details>
        </fieldset>
        <div className="quote-design-note">
          <strong>Your current design</strong>
          <p>{receipt ? "Your source repository is attached to the CNC request."
            : started ? "Retry sends the same request. Open a new viewer to change it."
              : "Your selections stay here while you review your design. Nothing has been sent."}</p>
        </div>
        <button className="quote-submit" type="submit"
          disabled={!delivery.enabled || !selected.machining || !this.props.preview || sending || Boolean(receipt)}
          aria-describedby="quote-availability">
          {receipt ? "CNC request sent" : sending ? "Sending…" : started ? "Retry CNC request"
            : delivery.sign_in_required ? "Sign in and send CNC request" : "Send CNC quote request"} <span aria-hidden="true">→</span>
        </button>
        <QuoteDeliveryStatus delivery={delivery} receipt={receipt} error={error} sending={sending} selected={selected} />
      </form>
    );
  }
}
