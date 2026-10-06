import fs from 'node:fs/promises';
import crypto from 'node:crypto';
import {Workbook} from '@oai/artifact-tool';
const path='work/audiopicture/hardware/bom/audiopicture-v2.2-rev-a.csv';
const source=await fs.readFile(path,'utf8');
const wb=await Workbook.fromCSV(source,{sheetName:'BOM'});
const sheet=wb.worksheets.getItem('BOM');
const before=structuredClone(sheet.getRange('A1:F75').values);
if(before.length!==75 || before[0].join('|')!=='Reference|PCB|Manufacturer Part Number|Qty|Function|Status')throw Error('Unexpected source shape');
// Formatting is only for the temporary preview: the deliverable remains CSV.
for(const [c,w] of [['A',125],['B',90],['C',280],['D',55],['E',300],['F',360]])sheet.getRange(`${c}1:${c}75`).format.columnWidthPx=w;
sheet.getRange('A1:F75').format.wrapText=true;
sheet.getRange('A1:F75').format.rowHeightPx=50;
const preview=async name=>{
 const png=await wb.render({sheetName:'BOM',range:'A32:F41',scale:1,format:'png'});
 await fs.writeFile(`work/${name}.png`,new Uint8Array(await png.arrayBuffer()));
};
if(process.argv.includes('--preview-only')){await preview('bom-before');process.exit(0);}
const replacements={C901:['Panasonic EEU-FR1V471B','SELECTED_MPN_LEAD_FORM_RIPPLE_THERMAL_VALIDATE'],'L901-L904':['Coilcraft XAL7050-103MEC','SELECTED_MPN_DML_LOSS_THERMAL_VALIDATE']};
let edited=0;
for(let i=1;i<before.length;i++){
 const update=replacements[before[i][0]];if(!update)continue;
 sheet.getRange(`C${i+1}`).values=[[update[0]]];sheet.getRange(`F${i+1}`).values=[[update[1]]];edited++;
}
if(edited!==2)throw Error('Expected exactly two selected MPN rows');
await wb.recalculate();
const after=sheet.getRange('A1:F75').values,changes=[];
for(let i=0;i<75;i++)for(let j=0;j<6;j++)if(before[i][j]!==after[i][j]){
 if(!replacements[before[i][0]] || ![2,5].includes(j))throw Error('Unintended cell change');
 changes.push({row:i+1,column:j+1,reference:before[i][0],before:before[i][j],after:after[i][j]});
}
if(changes.length!==4)throw Error('Expected four changed cells');
await preview('bom-after');
// Serialize values authored through artifact-tool, preserving unaffected source lines exactly.
const lines=source.split(/\r?\n/),quote=v=>/[",\n\r]/.test(String(v))?'"'+String(v).replaceAll('"','""')+'"':String(v);
if(lines.filter(x=>x.length).length!==75)throw Error('Multiline CSV requires different serialization');
for(const row of new Set(changes.map(x=>x.row)))lines[row-1]=after[row-1].map(quote).join(',');
const result=lines.join(source.includes('\r\n')?'\r\n':'\n');
const reread=await Workbook.fromCSV(result,{sheetName:'Verify'});
if(JSON.stringify(reread.worksheets.getItem('Verify').getRange('A1:F75').values)!==JSON.stringify(after))throw Error('CSV round-trip mismatch');
await fs.writeFile(path,result);
await fs.writeFile('work/audiopicture/evidence/rev-ex/bom-reconciliation.json',JSON.stringify({classification:'DOCUMENTED_MPN_RECONCILIATION_NOT_APPLICATION_QUALIFICATION',source_sha256:crypto.createHash('sha256').update(source).digest('hex'),output_sha256:crypto.createHash('sha256').update(result).digest('hex'),changes,preserved_other_cells:true,rows:74},null,2));
console.log(JSON.stringify({changed_cells:changes.length,rows:74,round_trip_verified:true}));
