/** Scope: Connect public showcase controls, model loading and visible status. */
import { ShowcaseModel } from "./ShowcaseModel.js";
import { ShowcaseScene } from "./ShowcaseScene.js";

class ShowcaseApp {
  constructor() {
    this.status = document.querySelector("#status");
    this.doors = document.querySelector("#doors");
    this.buttons = [...document.querySelectorAll("[data-pose]")];
    const requested = new URLSearchParams(location.search).get("view");
    this.mode = requested === "exploded" ? requested : "assembled";
    this.view = new ShowcaseScene(document.querySelector("#stage"));
    this.model = new ShowcaseModel();
    // One external boundary handles download, decompression and invalid model data.
    this.model.load().then(() => this.ready()).catch(() => {
      this.status.textContent = "The 3D model could not load. Please reload to retry in a current browser.";
    });
  }

  ready() {
    this.view.scene.add(this.model.scene);
    this.status.hidden = true;
    document.querySelectorAll("button, input").forEach(control => { control.disabled = false; });
    for (const button of this.buttons) {
      button.addEventListener("click", () => { this.mode = button.dataset.pose; this.update(); });
    }
    this.doors.addEventListener("change", () => this.update());
    document.querySelector("#fit").addEventListener("click", () => this.update());
    this.update();
  }

  update() {
    for (const button of this.buttons) button.setAttribute("aria-pressed", String(button.dataset.pose === this.mode));
    const captions = {
      assembled: this.doors.checked ? "101 panel pieces + 511 hardware components · doors shown" : "101 panel pieces + 511 hardware components · door panels hidden",
      exploded: "Panels separated for inspection · not an assembly sequence",
    };
    document.querySelector("#caption").textContent = captions[this.mode];
    this.view.frame(this.model.pose(this.mode, this.doors.checked));
  }
}

// Catch only renderer initialization failures such as unavailable WebGL.
try { new ShowcaseApp(); }
catch { document.querySelector("#status").textContent = "This preview needs WebGL. Open it in a browser with graphics acceleration enabled."; }
