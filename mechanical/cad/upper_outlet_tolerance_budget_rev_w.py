# Rear-shell upper vent tolerance budget Rev.W
# No process capability is assumed. Computes allowable combinations from the 1.0 mm geometric budget.
import json
W_NOM=4.0
W_MIN=3.0
BUDGET=W_NOM-W_MIN

# Worst-case web loss model:
# loss = slot_A_edge_error + slot_B_edge_error + relative_position_error + local_warp_error
# Each term is non-negative consumption toward the web.
# If slot width tolerance is specified symmetrically as +/- Tw on each slot,
# the edge contribution toward a shared web is Tw/2 per slot when width is
# centered on its nominal centerline; total width contribution = Tw.
def remaining(relative_position, local_warp, slot_width_total_tol):
    loss=relative_position+local_warp+slot_width_total_tol
    return W_NOM-loss, BUDGET-loss

# Parametric requirement table only; values are scenarios, NOT process claims.
scenarios=[]
for pos in (0.2,0.3,0.4,0.5):
  for warp in (0.1,0.2,0.3):
    allowable_width=BUDGET-pos-warp
    scenarios.append({
      "relative_position_budget_mm":pos,
      "local_warp_budget_mm":warp,
      "max_combined_slot_width_contribution_mm":round(allowable_width,3),
      "feasible":allowable_width>=0
    })
print(json.dumps({
 "nominal_web_mm":W_NOM,
 "required_minimum_web_mm":W_MIN,
 "total_worst_case_loss_budget_mm":BUDGET,
 "equation":"W_min_actual = 4.0 - (E_width_pair + E_relative_position + E_local_warp)",
 "release_condition":"E_width_pair + E_relative_position + E_local_warp <= 1.0 mm",
 "scenarios_are_process_claims":False,
 "scenarios":scenarios
},indent=2))
