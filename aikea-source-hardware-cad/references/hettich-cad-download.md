# Download exact Hettich CAD

Execute this procedure for Hettich hardware before replacing exact CAD with a
preview or handing the whole download task to the user. The STEP route succeeded
for KA 4532 article **9114274** on 2026-09-15; its product reference records the
download checksum and imported solids. Apply the procedure to the active article,
not its dimensions or geometry. Portal behaviour can change between sessions.

## Choose the correct entry point

Read the matching product reference for its official configured link:

| Product | Article | Reference |
| --- | --- | --- |
| SL 322 hanging-rail support | 70664 | [Support](hettich-sl322.md) |
| KA 4532, 400 mm | 9114274 | [Runner](hettich-ka-4532-400.md) |
| KA 4532, 500 mm and spacer | 9114276, 13952 | [Runner and spacer](hettich-ka-4532-spacer.md) |
| KA 5332, 500 mm | 9057405 | [Runner](hettich-ka-5332.md) |

For another article, follow **Hettich CAD** from its official product page. Do not
guess the family path or reuse another article's temporary ZIP URL.

## Execute the browser flow

1. With browser tools, open the configured link yourself. Confirm the **Order
   number** in the visible product table, plus any length and handedness choices.
   A family title or URL containing the right number is insufficient: the table
   can still default to a different article.
2. Click **CAD**. If no format is selected, use **Formats → Add formats**.
3. Select **Download**, not **CAD Direct Integration with PART2cad**. Select
   **STEP AP214 (3D)**. Confirm it appears under **Your selection**. If the
   checkbox action does nothing, inspect the visible control and click the green
   **+** or format label; do not repeatedly click an invisible checkbox.

   ![STEP AP214 selected in the successful 9114274 session; example controls, not the article to choose for every project](../assets/ka4532-400/format.png)

4. Click **CAD** again to generate the file. In **Files / Prepared files**, wait
   until generation has finished and **Download** appears beside the exact
   article. A pending generation is not a login or unsupported-product blocker.
5. Click **Download** in that browser session. Check its download result and the
   destination directory. Confirm a completed ZIP exists on disk, not just a
   prepared-file row or a download click.

   ![Finished generation with Download beside 9114274; example of the completed portal state](../assets/ka4532-400/download.png)

These are actual screenshots from the runner download. For another product,
explain the different article number; do not present them as current screenshots
of the rail support or fabricate a successful download image.

## Recover a failed download

- A direct HTTP **403** does not prove browser download is unavailable. The
  successful 9114274 run had this exact difference. Return to the normal portal
  session and download its prepared file there.
- If the browser reports a blocked or failed download, inspect the actual
  browser download result and any new window. Use another available, authorised
  browser/download capability if the current tool cannot save files. Do not
  disable browser protections, bypass access controls or retry the same failed
  temporary URL indefinitely.
- If authentication opens separately, inspect the browser's other windows/tabs.
  Ask the user only for the observed authentication, agreement or other action
  that requires them; after it is completed, resume the remaining steps yourself.
- Without browser tools, provide the exact configured product link and these
  visual steps, one action at a time. Explain that the exact CAD is needed to
  verify the purchased fitting and complete its installation. With browser tools
  but a user-only final step, leave that configured page ready for them.
- If STEP retrieval remains unavailable, inspect the official product's public
  CAD archive. A 3D DXF containing ACIS can be input to a verified conversion;
  it is not already STEP. Follow [hardware recovery](resolve-missing-hardware.md).
  Keep the feature required and record the precise next action. A dimensioned
  preview does not close the sourcing task.

## Finish criteria

Do not report the CAD acquisition complete until all of these hold:

1. The original download exists locally and contains the intended STEP, rather
   than an HTML error page, only a 2D drawing, or an incomplete browser download.
2. The article matches the active selection. Preserve the original archive and
   notices; run `store_hardware_cad.py` with the manufacturer, product family,
   article, official source links and downloaded file as shown in the main skill.
3. Import the STEP with the installed CAD runtime. Record its checksum, units,
   valid solid count and native bounds. Compare known product datums and any
   registered source checksum; investigate differences rather than accepting
   changed geometry silently. Never rescale hardware to make it fit.
4. Return the exact stored source to the owning construction module, replace any
   temporary preview, and resume placement, fixing and fit checks. Source success
   is not installation approval, and an unfinished installation is still work.
