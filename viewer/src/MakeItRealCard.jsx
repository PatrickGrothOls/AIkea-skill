/** Scope: Open and dismiss the quote page while preserving the design and form. */

import { Component, createRef } from "react";
import { QuoteRequestPage } from "./QuoteRequestPage";
import "./ReviewActionCards.css";

export class MakeItRealCard extends Component {
  dialog = createRef();
  state = { preview: null };

  open = () => {
    let preview = null;
    // Canvas serialization can fail under the browser's image-origin rules.
    try {
      preview = this.props.capturePreview();
    } catch (error) {
      if (error.name !== "SecurityError") throw error;
    }
    this.setState({ preview }, () => {
      this.dialog.current.showModal();
      this.dialog.current.scrollTop = 0;
      this.dialog.current.querySelector("h1").focus();
      this.props.onOpenChange(true);
    });
  };

  close = () => {
    this.dialog.current.close();
  };

  render() {
    return (
      <section className="make-real-card" aria-label="Make this design real">
        <button className="make-real-action" type="button" disabled={!this.props.ready} onClick={this.open}>
          Make it real <span aria-hidden="true">↗</span>
        </button>
        <dialog ref={this.dialog} className="quote-dialog" aria-labelledby="quote-page-title"
          onClose={() => this.props.onOpenChange(false)}>
          <QuoteRequestPage preview={this.state.preview} title={this.props.title} onBack={this.close} />
        </dialog>
      </section>
    );
  }
}
