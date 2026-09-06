# Recessed linear lighting

## Design objective

Choose the fewest practical installed components while preserving a purchased,
finished appearance and deterministic machining. Prefer one complete made-to-
length recessed luminaire over a loose LED strip, channel, diffuser, clips, and
end caps when both options meet the furniture design.

The first proof uses Domus Line APEX 84 HI because its manufacturer describes it
as a complete recessed linear luminaire for wardrobe sides and publishes one
simple installation envelope. This is the first verified profile, not a universal
hardware choice for every future lighting situation.

## Verified first profile

Source: <https://www.domusline.com/product/apex-84/>

- Product: Domus Line APEX 84 HI
- Installation: through-milled groove, especially suitable for wardrobe sides
- Groove: 4 mm wide and 8 mm deep
- Supply: 24 VDC
- Nominal power: 10 W/m
- Available single-colour temperatures: 2900 K, 3200 K, and 4300 K
- Supplied cable: 2000 mm
- Length: made to request
- Power supply: not included and kept remote from this panel proof

The viewer may export separate `body` and `emitter` meshes so it can show the
same purchased item switched off and on. Those meshes are one purchased
luminaire, not separate manufactured or ordered parts.

## Placement authority

Save one run in the host part's local face plane, with positive Z pointing out
from the finished face. Its start and end points are the
single placement authority for:

- the CadQuery groove cutter;
- the purchased-luminaire envelope;
- the Three.js area light and visible emitter.

The groove belongs to the host part because it changes that part's geometry. It
does not belong in the global furniture specification or in a joint specification.
The furniture assembly only places the already-machined host part.

For a through-milled run, place both endpoints at the useful physical boundaries
of the host face. For a blind run or cable exit, use the exact installation data
for the selected product before adding geometry.

## Approval gates

Prove a new lighting profile on one standalone sheet first. Show the same model
with the light off and on. After that approval, apply one chosen run to one real
generated cabinet. The host part keeps the local run; the composed cabinet keeps
the purchased item and its calculated cabinet frame. Check the groove against
earlier machining and the purchased body against the cabinet's other parts.

Show that cabinet switched off and on. Do not repeat the feature across cabinets
until the client approves the position, purchased-light appearance, and light
effect in the actual furniture.

Electrical supply selection, mains wiring, certification, and custom electronics
remain outside this skill.
