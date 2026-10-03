/** Scope: Compose the quote page around the current design and local preferences. */

import { Component } from "react";
import { QuoteRequestForm } from "./QuoteRequestForm";
import "./QuoteRequestPage.css";

export class QuoteRequestPage extends Component {
  render() {
    const { preview, title, onBack } = this.props;
    return (
      <div className="quote-page">
        <header className="quote-header">
          <span className="quote-wordmark" aria-label="AIkea">AIkea</span>
          <ol className="quote-steps" aria-label="Quote process">
            <li aria-current="step"><span>1</span> Request quotes</li>
            <li><span>2</span> Compare offers</li>
            <li><span>3</span> Order</li>
          </ol>
          <button className="quote-close" type="button" onClick={onBack} aria-label="Back to my design">×</button>
        </header>
        <div className="quote-layout">
          <section className="quote-preview" aria-label="Current furniture design">
            <h1 id="quote-page-title" tabIndex={-1}>Your furniture, made real.</h1>
            <p className="quote-subtitle">Get quotes for the help you need.</p>
            <div className="quote-preview-image">
              {preview ? <img src={preview} alt={`Current view of ${title}`} />
                : <p>The design preview is unavailable. Your design is still in the viewer.</p>}
            </div>
            <div className="quote-preview-caption">
              <div><strong>{title}</strong><p>Current design preview</p></div>
              <button className="quote-back" type="button" onClick={onBack}>← Back to design</button>
            </div>
          </section>
          <QuoteRequestForm preview={preview} title={title} />
        </div>
      </div>
    );
  }
}
