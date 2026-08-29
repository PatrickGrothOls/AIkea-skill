# Hettich KA 5332 drawer hardware

Use this reference for the visually approved 500 mm KA 5332 prototype.

## Local source

Obtain article `9057405` through `$aikea-source-hardware-cad`. Pass its returned
`hardware_directory` directly to the Hettich generator. The expected project
directory ends in:

```text
hardware/hettich/ka-5332/9057405/source
```

Do not ask for or pass an individual STEP path. `HettichKa5332StepAssemblyLoader`
selects `9057405.stp` through the public product manifest, checks its approved
SHA-256 value, imports it unchanged, and verifies the six native solids and
bounds before classifying the paired runner members.

## Construction authority

`HettichKa5332RunnerProfile` owns the manufacturer planning values.
`HettichKa5332DrawerBoxProfileAdapter` converts the side clearance into generic
drawer-box sizing. `HettichKa5332MountingPlanner` places the cabinet and drawer
members from the cabinet's local faces. The review generator may compose those
results, but it must not replace their calculations.

The current KA 5332 output is a visually approved construction prototype. It
does not yet save the drawer as a cabinet-owned project child or claim mounting
machining and manufacturing readiness.
