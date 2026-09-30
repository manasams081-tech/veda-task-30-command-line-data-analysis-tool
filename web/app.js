const state = {action:"summary"};
const extra = document.getElementById("extra");
const resultTitle = document.getElementById("resultTitle");
const cards = document.getElementById("cards");
const tableWrap = document.getElementById("tableWrap");
const raw = document.getElementById("raw");
const command = document.getElementById("command");
const timeEl = document.getElementById("time");

const meta = {
  summary:["Dataset summary","--summary"],
  preview:["Dataset preview","--preview 10"],
  filter:["Filtered records","--filter REGION VALUE"],
  group:["Grouped analysis","--group REGION --metric SALES"],
  stats:["Descriptive statistics","--stats SALES"]
};

document.querySelectorAll(".op").forEach(btn=>{
  btn.addEventListener("click",()=>{
    document.querySelectorAll(".op").forEach(x=>x.classList.remove("active"));
    btn.classList.add("active");
    state.action=btn.dataset.action;
    renderExtra();
  });
});

function input(label,id,placeholder){
  return `<label>${label}<input id="${id}" placeholder="${placeholder}"></label>`;
}
function renderExtra(){
  if(state.action==="filter"){
    extra.innerHTML=input("Column","column","e.g. region")+input("Value","value","e.g. South");
  }else if(state.action==="group"){
    extra.innerHTML=input("Group column","column","e.g. region")+input("Metric (optional)","metric","e.g. sales");
  }else if(state.action==="stats"){
    extra.innerHTML=input("Numeric column","column","e.g. sales");
  }else{
    extra.innerHTML="";
  }
  updateCommand();
}
function updateCommand(){
  const file=document.getElementById("file").value;
  let suffix=meta[state.action][1];
  if(state.action==="filter"){
    const c=document.getElementById("column")?.value||"COLUMN";
    const v=document.getElementById("value")?.value||"VALUE";
    suffix=`--filter ${c} ${v}`;
  }else if(state.action==="group"){
    const c=document.getElementById("column")?.value||"COLUMN";
    const m=document.getElementById("metric")?.value||"";
    suffix=`--group ${c}${m?` --metric ${m}`:""}`;
  }else if(state.action==="stats"){
    const c=document.getElementById("column")?.value||"COLUMN";
    suffix=`--stats ${c}`;
  }
  command.textContent=`python cli_tool.py --file ${file} ${suffix}`;
}
extra.addEventListener("input",updateCommand);
document.getElementById("file").addEventListener("change",updateCommand);

document.getElementById("run").addEventListener("click",runAnalysis);

async function runAnalysis(){
  const params=new URLSearchParams({
    file:document.getElementById("file").value,
    action:state.action,
    limit:"20"
  });
  ["column","value","metric"].forEach(id=>{
    const el=document.getElementById(id); if(el) params.set(id,el.value);
  });
  resultTitle.textContent=meta[state.action][0];
  timeEl.textContent="Running…";
  cards.innerHTML=""; tableWrap.innerHTML=""; raw.style.display="none";
  try{
    const res=await fetch(`/api/analyze?${params.toString()}`);
    const data=await res.json();
    if(!data.ok) throw new Error(data.error);
    render(data.result);
    timeEl.textContent="Updated just now";
  }catch(err){
    tableWrap.innerHTML=`<div style="padding:18px;color:#b42318;font-size:12px">⚠ ${escapeHtml(err.message)}</div>`;
    timeEl.textContent="Error";
  }
}
function render(result){
  if(state.action==="summary"){
    const items=[
      ["Rows",result.rows],["Columns",result.columns],["Missing",result.missing_values],
      ["Numeric",result.numeric_columns.length]
    ];
    cards.innerHTML=items.map(([a,b])=>`<div class="card"><span>${a}</span><strong>${b}</strong></div>`).join("");
    tableWrap.innerHTML=makeTable(result.column_names.map((c,i)=>({index:i+1,column:c})));
    return;
  }
  if(state.action==="stats"){
    cards.innerHTML=[
      ["Count",result.count],["Mean",fmt(result.mean)],["Median",fmt(result.median)],
      ["Min",fmt(result.min)],["Max",fmt(result.max)],["Sum",fmt(result.sum)]
    ].map(([a,b])=>`<div class="card"><span>${a}</span><strong>${b}</strong></div>`).join("");
    return;
  }
  tableWrap.innerHTML=makeTable(Array.isArray(result)?result:[]);
}
function makeTable(rows){
  if(!rows.length) return `<div style="padding:18px;color:#68758a;font-size:12px">No records found.</div>`;
  const cols=[...new Set(rows.flatMap(r=>Object.keys(r)))];
  return `<table><thead><tr>${cols.map(c=>`<th>${escapeHtml(c)}</th>`).join("")}</tr></thead><tbody>${
    rows.map(r=>`<tr>${cols.map(c=>`<td>${escapeHtml(r[c])}</td>`).join("")}</tr>`).join("")
  }</tbody></table>`;
}
function fmt(n){return Number(n).toLocaleString(undefined,{maximumFractionDigits:2})}
function escapeHtml(v){return String(v??"").replace(/[&<>"']/g,m=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#039;"}[m]))}
document.getElementById("copy").addEventListener("click",async()=>{
  await navigator.clipboard.writeText(command.textContent);
  document.getElementById("copy").textContent="Copied ✓";
  setTimeout(()=>document.getElementById("copy").textContent="Copy command",1200);
});
renderExtra();
runAnalysis();
