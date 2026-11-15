/** Scope: Present the product name without the previous image logo. */

import { Component } from "react";

export class ReviewBrand extends Component {
  render() {
    return (
      <span className="review-brand" aria-label="WardrobeAgentWizard">
        <span>Wardrobe</span><span>AgentWizard</span>
      </span>
    );
  }
}
