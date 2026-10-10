"""Check vendor CAD and distinguish nominal installation from FEA surrogates."""
from pathlib import Path
import hashlib
import json
import cadquery as cq

repo=Path(__file__).resolve().parents[2]
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
catalog_path=repo/'mechanical/components/ruthex-m4-insert-candidate-rev-fe.json'
catalog=json.loads(catalog_path.read_text())
source_path=repo/catalog['source']; sources=json.loads(source_path.read_text())
for s in sources['files']: assert sha(repo/s['file'])==s['sha256']
vendor=repo/'evidence/rev-fe/insert-source/ruthex_RX-M4x8.1.step'
model=cq.importers.importStep(str(vendor)); b=model.val().BoundingBox()
assert model.val().isValid() and model.solids().size()==1
frame_path=repo/'evidence/rev-eu21/execution.json'
frame=json.loads(frame_path.read_text())
depth=frame['bore_z_mm'][1]-frame['bore_z_mm'][0]
diameter=2*frame['bore_radius_seed_mm']
report={
    'classification':'CATALOG_AND_CALCULATED_CAD_NOT_MEASURED',
    'manufacturer_part':catalog['part_number'],
    'vendor_CAD_valid':True,'vendor_CAD_solids':1,'vendor_CAD_volume_mm3':model.val().Volume(),
    'vendor_CAD_Occ_bounding_box_mm':[b.xmin,b.xmax,b.ymin,b.ymax,b.zmin,b.zmax],
    'bounding_box_note':'The source thread-end/bounding surface exceeds nominal Z0. Retain source unchanged; do not turn this CAD bound into a manufacturing tolerance or replace the catalog L=8.1 mm.',
    'surrogate_frame_revision':frame['revision'],
    'surrogate_bore_diameter_mm':diameter,'surrogate_bore_depth_mm':depth,
    'catalog_nominal_installation_hole_mm':catalog['manufacturer_nominal_installation_hole_diameter_mm'],
    'catalog_min_installation_depth_mm':catalog['manufacturer_min_hole_depth_mm'],
    'surrogate_depth_shortfall_mm':catalog['manufacturer_min_hole_depth_mm']-depth,
    'surrogate_hole_diameter_difference_mm':diameter-catalog['manufacturer_nominal_installation_hole_diameter_mm'],
    'installation_specification_status':'FAIL_FOR_THIS_CATALOG_CANDIDATE',
    'production_selection_status':'OPEN: installation, pullout, torque, hot properties and frame integration not qualified',
    'source_sha256':{str(q.relative_to(repo)):sha(q) for q in [vendor,catalog_path,source_path,frame_path,Path(__file__)]}
}
out=repo/'evidence/rev-fe/insert-source/cad-audit.json'
out.write_text(json.dumps(report,indent=2)+'\n'); print(json.dumps(report,indent=2))
