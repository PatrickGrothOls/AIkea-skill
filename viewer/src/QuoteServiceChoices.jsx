/** Scope: Present furniture service choices and painting preferences. */

import { Component } from "react";

const services = [
  { id: "machining", title: "CNC machining", detail: "Your design cut into ready-to-assemble parts." },
  { id: "painting", title: "Painting", detail: "Your parts painted in your chosen colour." },
  { id: "installation", title: "Home installation", detail: "Assembly and fitting in your home." },
];

export class QuoteServiceChoices extends Component {
  render() {
    const { selected, finish, colour, onToggle, onChange } = this.props;
    return (
      <fieldset className="quote-services">
        <legend>What would you like help with?</legend>
        <p>Choose one service or the complete package.</p>
        {services.map(({ id, title, detail }) => (
          <div key={id} className={`quote-service ${selected[id] ? "is-selected" : ""}`}>
            <label className="quote-service-choice">
              <input type="checkbox" name={id} checked={selected[id]} onChange={() => onToggle(id)} />
              <span><strong>{title}</strong><span>{detail}</span></span>
            </label>
            {id === "painting" && selected.painting && (
              <div className="quote-paint-preferences">
                <label>Colour &amp; finish
                  <select name="finish" value={finish} onChange={onChange}>
                    <option value="discuss">Decide with the painter</option>
                    <option value="specified">I have a colour in mind</option>
                  </select>
                </label>
                {finish === "specified" && <label>Colour and finish preference
                  <input name="colour" value={colour} onChange={onChange}
                    placeholder="For example, warm white with a matt finish" maxLength={200} />
                </label>}
              </div>
            )}
          </div>
        ))}
      </fieldset>
    );
  }
}
