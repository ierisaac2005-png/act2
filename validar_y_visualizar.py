"""Valida el OWL, consulta casos y genera vistas auxiliares (no OntoGraf).
Ejecutar: python validar_y_visualizar.py. Requiere Java para HermiT.
"""
from pathlib import Path
import sys, platform, importlib.metadata
from rdflib import Graph, Namespace
from rdflib.namespace import RDF, RDFS, OWL
from owlready2 import World, sync_reasoner
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

HERE=Path(__file__).resolve().parent
N=Namespace('https://example.org/softtek-academico/soporte-ti#')
g=Graph().parse(HERE/'softtek_soporte_ti.owl')
def local(x): return str(x).split('#')[-1]
lines=['VALIDACIÓN REAL DEL MODELO — caso académico Softtek',
       'Generación y razonamiento fuera de Protégé; no es evidencia de OntoGraf.',
       f'Python: {platform.python_version()}']
for package in ['rdflib','owlready2','matplotlib']:lines.append(f'{package}: {importlib.metadata.version(package)}')
for label,kind,expected in [('Clases',OWL.Class,10),('Object Properties',OWL.ObjectProperty,7),('Data Properties',OWL.DatatypeProperty,10),('Individuos',OWL.NamedIndividual,15)]:
 count=len(set(g.subjects(RDF.type,kind)));assert count==expected,(label,count)
 lines.append(f'{label}: {count}')
assert len(list(g.triples((None,RDFS.subClassOf,None))))==4
lines.append('Jerarquías: 4 relaciones de subclase.')
for prop in g.subjects(RDF.type,OWL.ObjectProperty):
 assert g.value(prop,RDFS.domain) is not None and g.value(prop,RDFS.range) is not None
for i in g.subjects(RDF.type,N.Incidente):
 assert 1<=int(g.value(i,N.nivelPrioridad))<=4
 assert str(g.value(i,N.estado)) in ['Abierto','Resuelto']
 assert g.value(i,N.codigoIncidente) is not None
lines.append('Dominios/rangos y datos de los tres incidentes: correctos.')
world=World();onto=world.get_ontology((HERE/'softtek_soporte_ti.owl').as_uri()).load()
sync_reasoner(world,debug=0)
assert not list(world.inconsistent_classes())
assert onto.Sistema in onto.PortalClientes.INDIRECT_is_a
assert onto.Documento in onto.ProcedimientoAcceso.INDIRECT_is_a
lines += ['HermiT: ontología consistente; ninguna clase insatisfacible.',
          'Inferencia comprobada: PortalClientes es Sistema por Aplicacion.',
          'Inferencia comprobada: ProcedimientoAcceso es Documento por Procedimiento.']
query='''PREFIX sti: <https://example.org/softtek-academico/soporte-ti#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
SELECT ?nuevo ?sistema ?anterior ?documento ?tecnico WHERE {
 ?nuevo sti:estado "Abierto"^^xsd:string; sti:afecta ?sistema .
 ?anterior sti:estado "Resuelto"^^xsd:string; sti:afecta ?sistema .
 ?documento sti:documenta ?anterior; sti:describe ?sistema .
 ?tecnico sti:resuelve ?anterior .
} ORDER BY ?nuevo ?documento'''
# Se usa xsd:string explícito para coincidir con los literales serializados.
rows=[tuple(local(v) for v in row) for row in g.query(query)]
assert rows==[('INC003','PortalClientes','INC001','ProcedimientoAcceso','AnaTorres')],rows
lines += ['Consulta SPARQL (reutilización por sistema compartido):',
          'nuevo | sistema | anterior | documento | tecnico']
lines += [' | '.join(row) for row in rows]
lines += ['Interpretación: documento candidato para INC003, no resolución automática.',
          'Protégé y exportación OntoGraf: PENDIENTES en el equipo del estudiante.']
(HERE/'VALIDACION.txt').write_text('\n'.join(lines)+'\n',encoding='utf-8')

def plot_graph(filename,title,labels,edges,subtitle):
 fig,ax=plt.subplots(figsize=(14,8.5));ax.set_xlim(-1.5,9.5);ax.set_ylim(-2.8,5.3);ax.axis('off')
 fig.patch.set_facecolor('white')
 positions={'Tecnico':(0,3),'Herramienta':(4,3),'Area':(8,3),
            'Incidente':(0,0),'Documento':(4,0),'Sistema':(8,0),'Servidor':(8,-2)}
 def arrow(a,b,label,rad=0,offset=(0,0)):
  x1,y1=positions[a];x2,y2=positions[b]
  if a==b:
   # Dependencia entre dos individuos de Sistema, no autorrelación obligatoria.
   start=(x1+.55,y1+.6);end=(x1-.55,y1+.6)
   patch=FancyArrowPatch(start,end,connectionstyle='arc3,rad=1.4',arrowstyle='-|>',mutation_scale=15,color='black',lw=1.4)
   ax.add_patch(patch);ax.text(x1,y1+1.7,label,ha='center',va='center',fontsize=11)
   return
  import math
  dx=x2-x1;dy=y2-y1
  # Same-sized boxes with padded arrow endpoints; large curved top/bottom edges.
  if rad:
   start=(x1,y1+(.62 if rad>0 else -.62));end=(x2,y2+(.62 if rad>0 else -.62))
  elif abs(dx)>abs(dy):
   start=(x1+1.37*(1 if dx>0 else -1),y1);end=(x2-1.37*(1 if dx>0 else -1),y2)
  else:
   start=(x1,y1+.62*(1 if dy>0 else -1));end=(x2,y2-.62*(1 if dy>0 else -1))
  ax.add_patch(FancyArrowPatch(start,end,connectionstyle=f'arc3,rad={-rad}',arrowstyle='-|>',mutation_scale=15,color='black',lw=1.4))
  tx=(x1+x2)/2+offset[0];ty=(y1+y2)/2+offset[1]
  ax.text(tx,ty,label,ha='center',va='center',fontsize=11,bbox=dict(facecolor='white',edgecolor='none',pad=2))
 for a,b,label,rad,offset in edges:arrow(a,b,label,rad,offset)
 for key,txt in labels.items():
  x,y=positions[key]
  ax.add_patch(FancyBboxPatch((x-1.3,y-.52),2.6,1.04,boxstyle='round,pad=0.07',facecolor='white',edgecolor='black',lw=1.5))
  for j,line in enumerate(txt.split('\n')):
   ax.text(x,y+.25-j*.26,line,ha='center',va='center',fontsize=12 if j==0 else 10,fontweight='bold' if j==0 else 'normal')
 ax.set_title(title,fontsize=19,fontweight='bold',pad=18)
 fig.text(.5,.045,subtitle,ha='center',fontsize=10)
 fig.savefig(HERE/filename,dpi=180,bbox_inches='tight');plt.close(fig)

schema_edges=[('Tecnico','Herramienta','utiliza',0,(0,.18)),('Tecnico','Area','perteneceA',.25,(0,1.7)),
 ('Tecnico','Incidente','resuelve',0,(.48,0)),('Documento','Incidente','documenta',0,(0,.18)),
 ('Documento','Sistema','describe',0,(0,.18)),('Incidente','Sistema','afecta',-.25,(0,-1.7)),
 ('Sistema','Sistema','dependeDe',0,(0,0))]
# Las siete aristas representan los dominios y rangos efectivos del OWL.
for a,b,p,_,__ in schema_edges:
 assert (N[p],RDFS.domain,N[a]) in g and (N[p],RDFS.range,N[b]) in g
plot_graph('grafo_modelo.png','Ontología de soporte TI | Caso académico Softtek',{
 'Tecnico':'Tecnico\nPersona de soporte','Herramienta':'Herramienta\nDiagnóstico o intervención','Area':'Area\nUnidad organizacional',
 'Incidente':'Incidente\nFalla registrada','Documento':'Documento\nSubclases: Manual\ny Procedimiento','Sistema':'Sistema\nSubclases: Aplicacion\ny Servidor'},schema_edges,
 'Vista de esquema: nodos = clases; flechas = Object Properties (dominio → rango).\nDependeDe conecta sistemas; no exige que un sistema dependa de sí mismo. Vista generada con Python, no OntoGraf.')
case_edges=[('Tecnico','Herramienta','utiliza',0,(0,.18)),('Tecnico','Area','perteneceA',.25,(0,1.7)),
 ('Tecnico','Incidente','resuelve',0,(.48,0)),('Documento','Incidente','documenta',0,(0,.18)),
 ('Documento','Sistema','describe',0,(0,.18)),('Incidente','Sistema','afecta',-.25,(0,-1.7)),
 ('Sistema','Servidor','dependeDe',0,(.65,0))]
case={'Tecnico':'AnaTorres','Herramienta':'ConsolaIdentidad','Area':'MesaServicio','Incidente':'INC001','Documento':'ProcedimientoAcceso','Sistema':'PortalClientes','Servidor':'ServidorAplicaciones'}
for a,b,p,_,__ in case_edges:assert (N[case[a]],N[p],N[case[b]]) in g
plot_graph('grafo_caso.png','Grafo de conocimiento | Resolución de INC001',{
 k:case[k]+'\n'+({'Sistema':'Aplicacion','Servidor':'Servidor','Documento':'Procedimiento'}.get(k,k)) for k in case},case_edges,
 'Vista de un caso: nodos = individuos ficticios; flechas = relaciones afirmadas en el archivo OWL.\nMuestra 7 de los 15 individuos del modelo. Vista generada con Python, no OntoGraf.')
print('\n'.join(lines))
print('Imágenes generadas: grafo_modelo.png y grafo_caso.png')
