from django.shortcuts import render
from SPARQLWrapper import SPARQLWrapper, JSON
from .forms import other, ActorMetrics, NetworkMetrics, filtroKnowledgeArea, filtroNetworkMetrics, filtroActorsMetrics, PeriodicOther, filtroPeriodic, filtroEvent, EventOther, InstitutionOther, filtroInstitution, PGPOther, FiltroPGP, GeographicOther, FiltroGeographic

# Create your views here.
def home(request):
	sparql = SPARQLWrapper("http://localhost:3030/SCNAS")
	consulta = ("""
prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#>
prefix owl: <http://www.w3.org/2002/07/owl#>
PREFIX xmlns:<http://www.nanopub.org/nschema>
PREFIX base:<http://www.nanopub.org/nschema>
PREFIX dc:<http://purl.org/dc/elements/1.1/>
PREFIX np:<http://www.nanopub.org/nschema#>
PREFIX ns:<http://www.w3.org/2003/06/sw-vocab-status/ns#>
PREFIX owl:<http://www.w3.org/2002/07/owl#>
PREFIX xml:<http://www.w3.org/XML/1998/namespace>
PREFIX foaf:<http://xmlns.com/foaf/0.1/>
PREFIX prov:<http://www.w3.org/ns/prov#>
PREFIX rdfg:<http://www.w3.org/2004/03/trix/rdfg-1/>
PREFIX skos:<http://www.w3.org/2004/02/skos/core#>
PREFIX time:<http://www.w3.org/2006/time#>
PREFIX fabio:<http://purl.org/spar/fabio/>
PREFIX terms:<http://purl.org/dc/terms/>
PREFIX datacite:<http://purl.org/spar/datacite/>
PREFIX SNAMetric:<http://ns.inria.fr/semsna/2009/06/21/SNAMetric#>
PREFIX XMLSchema:<http://www.w3.org/2000/10/XMLSchema#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX scnas:<http://www.semanticweb.org/cliente/ontologies/2019/9/SCNAS#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX sc: <http://purl.org/science/owl/sciencecommons/>

SELECT  *
WHERE{
 ?nanopublication np:hasAssertion ?assertion .
 ?nanopublication np:hasProvenance ?provenance .
 ?provenance datacite:usesIdentifierScheme ?DOI .
 ?DOI fabio:hasURL ?URL .
 ?provenance dc:title ?title .
 ?assertion rdf:type np:Assertion .
 ?assertion scnas:has_Type ?type .
 ?type rdf:type scnas:Knowledge_Area.

""")

	listaActor=[]
	listaDC= []
	listaCC= []
	listaBC= []
	listaURL= []
	listaTitulos= []
	listaRegion= []


	listaTitle= []
	listaDensity= []
	listaComponentes= []
	listaAverageDegree = []
	ListaLocation= []
	listaActorsNumber = []
	listaEdgesNumber= []
	listaAC=[]
	aux=[]
	listaautores=[]
	listaresultados=[]
	listaresultado=[]
	listaAnoFim=[]
	listaAnoInicio=[]



	Location = "No"
	Betweenness = "No"
	Closeness = "No"
	Degree = "No"
	DOI = "No"
	#MÉTRICAS DE ATORES
	Actor="No"
	Densidade= "No"
	titulo = "No"
	Compo="No"
	Average= "No"
	AN= "No"
	EN= "No"
	AC="No"
	Titles="No"
	Inicio="No"
	Fim="No"
	counttitles = 0

	if request.method == "POST":
		if 'Network_Time_Begginning' in request.POST: #verifica se Degree_Centrality foi enviado na requisição
			Network_Time_Begginning = request.POST['Network_Time_Begginning']
			if Network_Time_Begginning:
				anoinicial = ("?inicio time:year " +Network_Time_Begginning+".")
				consulta+= ("""?assertion scnas:has_Network ?rede . 
				?rede scnas:has_Time ?tempo.
 				?tempo time:hasBeginning ?inicio .""" + anoinicial )

		if 'Network_Time' in request.POST: #verifica se Degree_Centrality foi enviado na requisição
			Network_Time = request.POST['Network_Time']
			if Network_Time:
				consulta+= ("""  ?assertion scnas:has_Network ?rede . 
				?rede scnas:has_Time ?tempo.
 				?tempo time:hasBeginning ?inicio .
 				?tempo time:hasEnd ?fim .
 				?inicio time:year ?anoinicio.
 				?fim time:year ?anofim .""" )
		if 'Knowledge_Area' in request.POST: #verifica se Degree_Centrality foi enviado na requisição
			Knowledge_Area = request.POST['Knowledge_Area']
			if Knowledge_Area:
				consulta+= ("  ?type rdf:type scnas:Knowledge_Area.  ?type SNAMetric:hasName ?nameType ." )

		if 'Betweenness_Centrality_less_than' in request.POST: #verifica se Degree_Centrality foi enviado na requisição
			Betweenness_Centrality_less_than = request.POST['Betweenness_Centrality_less_than']
			if Betweenness_Centrality_less_than:
				if  Betweenness_Centrality_less_than != "":
						texto = (""" FILTER( ?valueBC < """ + Betweenness_Centrality_less_than +") .")
						consulta+= ("?actor SNAMetric:hasSNAMetricBetweennessCentrality ?BetweennessCentrality . ?BetweennessCentrality SNAMetric:hasValue ?valueBC ." + texto)

		if 'Betweenness_Centrality_greater_than' in request.POST: #verifica se Degree_Centrality foi enviado na requisição
			Betweenness_Centrality_greater_than = request.POST['Betweenness_Centrality_greater_than']
			if Betweenness_Centrality_greater_than:
				if  Betweenness_Centrality_greater_than != "":
						texto = (""" FILTER( ?valueBC > """ + Betweenness_Centrality_greater_than +") .")
						consulta+= ("?actor SNAMetric:hasSNAMetricBetweennessCentrality ?BetweennessCentrality . ?BetweennessCentrality SNAMetric:hasValue ?valueBC ." + texto)

		if 'Closeness_Centrality_less_than' in request.POST: #verifica se Degree_Centrality foi enviado na requisição
			Closeness_Centrality_less_than = request.POST['Closeness_Centrality_less_than']
			if Closeness_Centrality_less_than:
				if  Closeness_Centrality_less_than != "":
						texto = (""" FILTER( ?valueCC < """ + Closeness_Centrality_less_than +") .")
						consulta+= ("?actor SNAMetric:hasSNAMetricClosenessCentrality ?ClosenessCentrality . ?ClosenessCentrality SNAMetric:hasValue ?valueCC ." + texto)

		if 'Closeness_Centrality_greater_than' in request.POST: #verifica se Degree_Centrality foi enviado na requisição
			Closeness_Centrality_greater_than = request.POST['Closeness_Centrality_greater_than']
			if Closeness_Centrality_greater_than:
				if  Closeness_Centrality_greater_than != "":
						texto = (""" FILTER( ?valueCC > """ + Closeness_Centrality_greater_than +") .")
						consulta+= ("?actor SNAMetric:hasSNAMetricClosenessCentrality ?ClosenessCentrality . ?ClosenessCentrality SNAMetric:hasValue ?valueCC ." + texto)

		if 'Degree_Centrality_less_than' in request.POST: #verifica se Degree_Centrality foi enviado na requisição
			Degree_Centrality_less_than = request.POST['Degree_Centrality_less_than']
			if Degree_Centrality_less_than:
				if  Degree_Centrality_less_than != "":
						texto = (""" FILTER( ?valueDC < """ + Degree_Centrality_less_than +") .")
						consulta+= ("?actor SNAMetric:hasSNAMetricDegreeCentrality ?DegreeCentrality . ?DegreeCentrality SNAMetric:hasValue ?valueDC ." + texto)


		if 'Degree_Centrality_greater_than' in request.POST: #verifica se Degree_Centrality foi enviado na requisição
			Degree_Centrality_greater_than = request.POST['Degree_Centrality_greater_than']
			if Degree_Centrality_greater_than:
				if  Degree_Centrality_greater_than != "":
						texto = (""" FILTER( ?valueDC > """ + Degree_Centrality_greater_than +") .")
						consulta+= ("?actor SNAMetric:hasSNAMetricDegreeCentrality ?DegreeCentrality . ?DegreeCentrality SNAMetric:hasValue ?valueDC ." + texto)

		if 'Average_Degree_less_than' in request.POST: #verifica se Degree_Centrality foi enviado na requisição
			Average_Degree_less_than = request.POST['Average_Degree_less_than']
			if Average_Degree_less_than:
				if  Average_Degree_less_than != "":
						texto = (""" FILTER( ?valorAverageDegree < """ + Average_Degree_less_than +") .")
						consulta+= ("?rede scnas:has_AverageDegree ?AverageDegree . ?AverageDegree SNAMetric:hasValue ?valorAverageDegree ." + texto)

		if 'Average_Degree_less_than' in request.POST: #verifica se Degree_Centrality foi enviado na requisição
			Average_Degree_less_than = request.POST['Average_Degree_less_than']
			if Average_Degree_less_than:
				if  Average_Degree_less_than != "":
						texto = (""" FILTER( ?valorAverageDegree < """ + Average_Degree_less_than +") .")
						consulta+= ("?rede scnas:has_AverageDegree ?AverageDegree . ?AverageDegree SNAMetric:hasValue ?valorAverageDegree ." + texto)


		if 'Average_Degree_greater_than' in request.POST: #verifica se Degree_Centrality foi enviado na requisição
			Average_Degree_greater_than = request.POST['Average_Degree_greater_than']
			if Average_Degree_greater_than:
				if  Average_Degree_greater_than != "":
						texto = (""" FILTER( ?valorAverageDegree > """ + Average_Degree_greater_than +") .")
						consulta+= (" ?rede scnas:has_AverageDegree ?AverageDegree . ?AverageDegree SNAMetric:hasValue ?valorAverageDegree . " + texto)

		if 'Component_less_than' in request.POST: #verifica se Degree_Centrality foi enviado na requisição
			Component_less_than = request.POST['Component_less_than']
			if Component_less_than:
				if  Component_less_than != "":
						texto = (""" FILTER( ?ValorComponent < """ + Component_less_than +") .")
						consulta+= (" ?rede SNAMetric:hasSNAMetricComponent ?Component . ?Component SNAMetric:hasValue ?ValorComponent . " + texto)

		if 'Component_greater_than' in request.POST: #verifica se Degree_Centrality foi enviado na requisição
			Component_greater_than = request.POST['Component_greater_than']
			if Component_greater_than:
				if  Component_greater_than != "":
						texto = (""" FILTER( ?ValorComponent > """ + Component_greater_than +") .")
						consulta+= (" ?rede SNAMetric:hasSNAMetricComponent ?Component . ?Component SNAMetric:hasValue ?ValorComponent . " + texto)

		if 'Density_less_than' in request.POST: #verifica se Degree_Centrality foi enviado na requisição
			Density_less_than = request.POST['Density_less_than']
			if Density_less_than:
				if  Density_less_than != "":
						texto = (""" FILTER( ?valorDensity < """ + Density_less_than +") .")
						consulta+= (" ?rede scnas:has_Density ?densidade . ?densidade SNAMetric:hasValue ?valorDensity . " + texto)

		if 'Density_greater_than' in request.POST: #verifica se Degree_Centrality foi enviado na requisição
			Density_greater_than = request.POST['Density_greater_than']
			if Density_greater_than:
				if  Density_greater_than != "":
						texto = (""" FILTER( ?valorDensity > """ + Density_greater_than +") .")
						consulta+= (" ?rede scnas:has_Density ?densidade . ?densidade SNAMetric:hasValue ?valorDensity . " + texto)

		if 'Region_Name' in request.POST: #verifica se Degree_Centrality foi enviado na requisição
			Region_Name = request.POST['Region_Name']
			if Region_Name:
				if  Region_Name != "":
						texto = (""" ?location SNAMetric:hasName '""" + Region_Name +"' .")
						consulta+= (" ?rede scnas:has_Location ?location . " + texto)			

		if 'Knowledge_Area_Name' in request.POST: #verifica se Degree_Centrality foi enviado na requisição
			Knowledge_Area_Name = request.POST['Knowledge_Area_Name']
			if Knowledge_Area_Name:
				if  Knowledge_Area_Name != "":
					texto = (""" ?type SNAMetric:hasName '""" + Knowledge_Area_Name +"' .")							
					consulta += (texto)		

		if 'Region' in request.POST: #verifica se Degree_Centrality foi enviado na requisição
 			Region = request.POST['Region']
 			if Region: 							
 				consulta += ("""
 				?assertion scnas:has_Network ?rede . 
				?rede scnas:has_Location ?location .
 				?location SNAMetric:hasName ?NameLocation .""")
		if 'Degree_Centrality' in request.POST or 'Closeness_Centrality' in request.POST or 'Betweenness_Centrality' in request.POST:
			consulta += ("""  ?assertion scnas:has_Network ?rede .  """)
			Actor= "Actor"
			consulta += ("""
					?rede scnas:has_Actor ?actor.
 					?actor SNAMetric:hasName ?nameActor .""")
			if 'Degree_Centrality' in request.POST: #verifica se Degree_Centrality foi enviado na requisição
	 			Degree_Centrality = request.POST['Degree_Centrality']
	 			if Degree_Centrality:
	 				Degree = "Degree Centrality " 							
	 				consulta += ("""
					?actor SNAMetric:hasSNAMetricDegreeCentrality ?DegreeCentrality .
					?DegreeCentrality SNAMetric:hasValue ?valueDC .""")
			if 'Closeness_Centrality' in request.POST: #verifica se Closeness_Centrality foi enviado na requisição
				Closeness_Centrality = request.POST['Closeness_Centrality']
				if Closeness_Centrality:
					Closeness = "Closeness Centrality "							
					consulta += ("""
					?actor SNAMetric:hasSNAMetricClosenessCentrality ?ClosenessCentrality .
					?ClosenessCentrality SNAMetric:hasValue ?valueCC .""")
			if 'Betweenness_Centrality' in request.POST: #verifica se Betweenness_Centrality foi enviado na requisição
				Betweenness_Centrality = request.POST['Betweenness_Centrality']
				if Betweenness_Centrality:
					Betweenness = "Betweenness Centrality "						
					consulta += ("""
					?actor SNAMetric:hasSNAMetricBetweennessCentrality ?BetweennessCentrality .
					?BetweennessCentrality SNAMetric:hasValue ?valueBC .""")

		if 'Density' in request.POST or 'Component' in request.POST or 	'Average_Degree' in request.POST or 'Actors_Number' in request.POST or 'Edges_Number' in request.POST:
			consulta+=(" ?assertion scnas:has_Network ?rede .")
			if 'Density' in request.POST: #verifica se Degree_Centrality foi enviado na requisição
	 			Density = request.POST['Density']
	 			if Density:
	 				Density_ = "Density"
	 				consulta += ("""
					?rede scnas:has_Density ?densidade .
		 			?densidade SNAMetric:hasValue ?valorDensity .""") 
			if 'Component' in request.POST: #verifica se Degree_Centrality foi enviado na requisição
	 			Component = request.POST['Component']
	 			if Component:
	 				consulta += ("""
					?rede SNAMetric:hasSNAMetricComponent ?Component .
	 				?Component SNAMetric:hasValue ?ValorComponent. """) 
			if 'Average_Degree' in request.POST: #verifica se Degree_Centrality foi enviado na requisição
	 			Average_Degree = request.POST['Average_Degree']
	 			if Average_Degree:
	 				consulta += ("""
					?rede scnas:has_AverageDegree ?AverageDegree .
					 ?AverageDegree SNAMetric:hasValue ?valorAverageDegree .""") 
			if 'Actors_Number' in request.POST: #verifica se Degree_Centrality foi enviado na requisição
	 			Actors_Number = request.POST['Actors_Number']
	 			if Actors_Number:
	 				consulta += ("""
					?rede scnas:has_ActorsNumber ?ActorsNumber .
	 				?ActorsNumber SNAMetric:hasValue ?ValueActorsNumber .""")
			if 'Edges_Number' in request.POST: #verifica se Degree_Centrality foi enviado na requisição
	 			Edges_Number = request.POST['Edges_Number']
	 			if Edges_Number:
	 				consulta += ("""
					?rede scnas:has_EdgesNumber ?EdgesNumber .
					?EdgesNumber SNAMetric:hasValue ?ValueEdgesNumber .""")


		consulta += ("""
		}
		LIMIT 10000""")

		sparql.setQuery(consulta)
		sparql.setReturnFormat(JSON)
		results = sparql.query().convert()
		Titles = "No"


		def remove_repetidos(lista):
		    l = []
		    for i in lista:
		        if i not in l:
		            l.append(i)
		    l.sort()
		    return l

		for result in results["results"]["bindings"]:
			for var in results["head"]["vars"]:
				if var == "anoinicio":
					Inicio = "Beginning"
					listaAnoInicio.append(result[var]['value'])
				if var == "anofim":
					Fim = "End"
					listaAnoFim.append(result[var]['value'])
	 	
				if var == "title":
					Titles = "SCNAS"
					listaTitulos.append(result[var]['value'])
					aux= remove_repetidos(listaTitulos)
					counttitles= len(aux)			
				if var == "URL":
					DOI= "DOI"
					listaURL.append(result[var]['value'])
				if var == "NameLocation":
					Location = "Location"
					listaRegion.append(result[var]['value'])
				if var == "nameType":
					AC= "Knowledge Area"
					listaAC.append(result[var]['value'])				
				if 'Degree_Centrality' in request.POST or 'Closeness_Centrality' in request.POST or 'Betweenness_Centrality' in request.POST:
					if var == "nameActor":
						listaActor.append(result[var]['value'])
					if 'Degree_Centrality' in request.POST: #verifica se Degree_Centrality foi enviado na requisição
			 			Degree_Centrality = request.POST['Degree_Centrality']
			 			if Degree_Centrality:
			 				if var == "valueDC":
			 					listaDC.append(result[var]['value'])
					if 'Closeness_Centrality' in request.POST: #verifica se Closeness_Centrality foi enviado na requisição
						Closeness_Centrality = request.POST['Closeness_Centrality']
						if Closeness_Centrality:
							if var == "valueCC":
								listaCC.append(result[var]['value'])
					if 'Betweenness_Centrality' in request.POST: #verifica se Betweenness_Centrality foi enviado na requisição
						Betweenness_Centrality = request.POST['Betweenness_Centrality']
						if Betweenness_Centrality:
							if var == "valueBC":
								listaBC.append(result[var]['value'])
				if 'Density' in request.POST or 'Component' in request.POST or 'Average_Degree' in request.POST or 'Actors_Number' in request.POST or 'Edges_Number' in request.POST:					

					if 'Density' in request.POST: #verifica se Betweenness_Centrality foi enviado na requisição
						Densidade= "Density"
						Density = request.POST['Density']
						if Density:
							if var == "valorDensity":
								listaDensity.append(result[var]['value'])
					if 'Component' in request.POST: #verifica se Betweenness_Centrality foi enviado na requisição
						Compo="Component"
						Component = request.POST['Component']
						if Component:
							if var == "ValorComponent":
								listaComponentes.append(result[var]['value'])
					if 'Average_Degree' in request.POST: #verifica se Betweenness_Centrality foi enviado na requisição
						Average_Degree = request.POST['Average_Degree']
						if Average_Degree:
							Average= "Average Degree"
							if var == "valorAverageDegree":
								listaAverageDegree.append(result[var]['value'])
					if 'Actors_Number' in request.POST: #verifica se Betweenness_Centrality foi enviado na requisição
						Actors_Number = request.POST['Actors_Number']
						if Actors_Number:
							AN= "Actors Number"
							if var == "ValueActorsNumber":
								listaActorsNumber.append(result[var]['value'])

					if 'Edges_Number' in request.POST: #verifica se Betweenness_Centrality foi enviado na requisição
						Edges_Number = request.POST['Edges_Number']
						if Edges_Number:
							EN= "Edges Number"
							if var == "ValueEdgesNumber":
								listaEdgesNumber.append(result[var]['value'])


	print(listaAnoFim)

	return render(request, "home.html", {'other':other, 'ActorMetrics': ActorMetrics, 'NetworkMetrics': NetworkMetrics, 'filtroKnowledgeArea':filtroKnowledgeArea, 'filtroNetworkMetrics': filtroNetworkMetrics, 'filtroActorsMetrics': filtroActorsMetrics, 'Atores': listaActor, 'DCs':listaDC, 'CCs':listaCC, 'BCs': listaBC, 'URLs': listaURL, 'Titulos': listaTitle, 'Densities': listaDensity, 'Componentes': listaComponentes, 'AverageDegrees': listaAverageDegree, "Regions": listaRegion, 
	'Location': Location, 'Betweenness': Betweenness, 'Closeness': Closeness, 'Degree': Degree, 'DOI': DOI, 'Locations': ListaLocation, 'Actor': Actor, 'Densidade':Densidade, 'titulo': titulo, 'Compo':Compo, 'Averag': Average, 'numerodeatores': listaActorsNumber, 'AN':AN, 'EN':EN, "numerodeedges": listaEdgesNumber, "AC": AC, "listaAC": listaAC, 'listaTitles': listaTitulos, "Titles":Titles, "counttitles":counttitles,'listaAnoFim':listaAnoFim, 'listaAnoInicio':listaAnoInicio,'Inicio':Inicio, 'Fim': Fim})
	

def Periodic(request):

	sparql = SPARQLWrapper("http://localhost:3030/SCNAS")
	consulta = ("""
prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#>
prefix owl: <http://www.w3.org/2002/07/owl#>
PREFIX xmlns:<http://www.nanopub.org/nschema>
PREFIX base:<http://www.nanopub.org/nschema>
PREFIX dc:<http://purl.org/dc/elements/1.1/>
PREFIX np:<http://www.nanopub.org/nschema#>
PREFIX ns:<http://www.w3.org/2003/06/sw-vocab-status/ns#>
PREFIX owl:<http://www.w3.org/2002/07/owl#>
PREFIX xml:<http://www.w3.org/XML/1998/namespace>
PREFIX foaf:<http://xmlns.com/foaf/0.1/>
PREFIX prov:<http://www.w3.org/ns/prov#>
PREFIX rdfg:<http://www.w3.org/2004/03/trix/rdfg-1/>
PREFIX skos:<http://www.w3.org/2004/02/skos/core#>
PREFIX time:<http://www.w3.org/2006/time#>
PREFIX fabio:<http://purl.org/spar/fabio/>
PREFIX terms:<http://purl.org/dc/terms/>
PREFIX datacite:<http://purl.org/spar/datacite/>
PREFIX SNAMetric:<http://ns.inria.fr/semsna/2009/06/21/SNAMetric#>
PREFIX XMLSchema:<http://www.w3.org/2000/10/XMLSchema#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX scnas:<http://www.semanticweb.org/cliente/ontologies/2019/9/SCNAS#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX sc: <http://purl.org/science/owl/sciencecommons/>

SELECT  *
WHERE{
 ?nanopublication np:hasAssertion ?assertion .
 ?nanopublication np:hasProvenance ?provenance .
 ?provenance datacite:usesIdentifierScheme ?DOI .
 ?DOI fabio:hasURL ?URL .
 ?provenance dc:title ?title .
 ?assertion rdf:type np:Assertion .
 ?assertion scnas:has_Type ?type .
 ?type rdf:type scnas:Periodic .

""")

	listaActor=[]
	listaDC= []
	listaCC= []
	listaBC= []
	listaURL= []
	listaTitulos= []
	listaRegion= []
	aux=[]

	listaTitle= []
	listaDensity= []
	listaComponentes= []
	listaAverageDegree = []
	ListaLocation= []
	listaActorsNumber = []
	listaEdgesNumber= []
	listaAC= []

	Location = "No"
	Betweenness = "No"
	Closeness = "No"
	Degree = "No"
	DOI = "No"
	#MÉTRICAS DE ATORES
	Actor="No"
	Densidade= "No"
	titulo = "No"
	Compo="No"
	Average= "No"
	AN= "No"
	EN= "No"
	AC= "No"
	Titles="No"
	counttitles = 0

	Fim= "No"
	Inicio="No"
	listaAnoInicio=[]
	listaAnoFim=[]

	if request.method == "POST":

		if 'Network_Time' in request.POST: #verifica se Degree_Centrality foi enviado na requisição
			Network_Time = request.POST['Network_Time']
			if Network_Time:
				consulta+= ("""  ?assertion scnas:has_Network ?rede . 
				?rede scnas:has_Time ?tempo.
 				?tempo time:hasBeginning ?inicio .
 				?tempo time:hasEnd ?fim .
 				?inicio time:year ?anoinicio.
 				?fim time:year ?anofim .""" )

		if 'Knowledge_Area' in request.POST: #verifica se Degree_Centrality foi enviado na requisição
			Knowledge_Area = request.POST['Knowledge_Area']
			if Knowledge_Area:
				consulta+= (" ?type scnas:has_KnowledgeArea ?AC . ?AC SNAMetric:hasName ?NameAC . " )

		if 'Betweenness_Centrality_less_than' in request.POST: #verifica se Degree_Centrality foi enviado na requisição
			Betweenness_Centrality_less_than = request.POST['Betweenness_Centrality_less_than']
			if Betweenness_Centrality_less_than:
				if  Betweenness_Centrality_less_than != "":
						texto = (""" FILTER( ?valueBC < """ + Betweenness_Centrality_less_than +") .")
						consulta+= ("?actor SNAMetric:hasSNAMetricBetweennessCentrality ?BetweennessCentrality . ?BetweennessCentrality SNAMetric:hasValue ?valueBC ." + texto)

		if 'Betweenness_Centrality_greater_than' in request.POST: #verifica se Degree_Centrality foi enviado na requisição
			Betweenness_Centrality_greater_than = request.POST['Betweenness_Centrality_greater_than']
			if Betweenness_Centrality_greater_than:
				if  Betweenness_Centrality_greater_than != "":
						texto = (""" FILTER( ?valueBC > """ + Betweenness_Centrality_greater_than +") .")
						consulta+= ("?actor SNAMetric:hasSNAMetricBetweennessCentrality ?BetweennessCentrality . ?BetweennessCentrality SNAMetric:hasValue ?valueBC ." + texto)

		if 'Closeness_Centrality_less_than' in request.POST: #verifica se Degree_Centrality foi enviado na requisição
			Closeness_Centrality_less_than = request.POST['Closeness_Centrality_less_than']
			if Closeness_Centrality_less_than:
				if  Closeness_Centrality_less_than != "":
						texto = (""" FILTER( ?valueCC < """ + Closeness_Centrality_less_than +") .")
						consulta+= ("?actor SNAMetric:hasSNAMetricClosenessCentrality ?ClosenessCentrality . ?ClosenessCentrality SNAMetric:hasValue ?valueCC ." + texto)

		if 'Closeness_Centrality_greater_than' in request.POST: #verifica se Degree_Centrality foi enviado na requisição
			Closeness_Centrality_greater_than = request.POST['Closeness_Centrality_greater_than']
			if Closeness_Centrality_greater_than:
				if  Closeness_Centrality_greater_than != "":
						texto = (""" FILTER( ?valueCC > """ + Closeness_Centrality_greater_than +") .")
						consulta+= ("?actor SNAMetric:hasSNAMetricClosenessCentrality ?ClosenessCentrality . ?ClosenessCentrality SNAMetric:hasValue ?valueCC ." + texto)

		if 'Degree_Centrality_less_than' in request.POST: #verifica se Degree_Centrality foi enviado na requisição
			Degree_Centrality_less_than = request.POST['Degree_Centrality_less_than']
			if Degree_Centrality_less_than:
				if  Degree_Centrality_less_than != "":
						texto = (""" FILTER( ?valueDC < """ + Degree_Centrality_less_than +") .")
						consulta+= ("?actor SNAMetric:hasSNAMetricDegreeCentrality ?DegreeCentrality . ?DegreeCentrality SNAMetric:hasValue ?valueDC ." + texto)


		if 'Degree_Centrality_greater_than' in request.POST: #verifica se Degree_Centrality foi enviado na requisição
			Degree_Centrality_greater_than = request.POST['Degree_Centrality_greater_than']
			if Degree_Centrality_greater_than:
				if  Degree_Centrality_greater_than != "":
						texto = (""" FILTER( ?valueDC > """ + Degree_Centrality_greater_than +") .")
						consulta+= ("?actor SNAMetric:hasSNAMetricDegreeCentrality ?DegreeCentrality . ?DegreeCentrality SNAMetric:hasValue ?valueDC ." + texto)

		if 'Average_Degree_less_than' in request.POST: #verifica se Degree_Centrality foi enviado na requisição
			Average_Degree_less_than = request.POST['Average_Degree_less_than']
			if Average_Degree_less_than:
				if  Average_Degree_less_than != "":
						texto = (""" FILTER( ?valorAverageDegree < """ + Average_Degree_less_than +") .")
						consulta+= ("?rede scnas:has_AverageDegree ?AverageDegree . ?AverageDegree SNAMetric:hasValue ?valorAverageDegree ." + texto)

		if 'Average_Degree_less_than' in request.POST: #verifica se Degree_Centrality foi enviado na requisição
			Average_Degree_less_than = request.POST['Average_Degree_less_than']
			if Average_Degree_less_than:
				if  Average_Degree_less_than != "":
						texto = (""" FILTER( ?valorAverageDegree < """ + Average_Degree_less_than +") .")
						consulta+= ("?rede scnas:has_AverageDegree ?AverageDegree . ?AverageDegree SNAMetric:hasValue ?valorAverageDegree ." + texto)


		if 'Average_Degree_greater_than' in request.POST: #verifica se Degree_Centrality foi enviado na requisição
			Average_Degree_greater_than = request.POST['Average_Degree_greater_than']
			if Average_Degree_greater_than:
				if  Average_Degree_greater_than != "":
						texto = (""" FILTER( ?valorAverageDegree > """ + Average_Degree_greater_than +") .")
						consulta+= (" ?rede scnas:has_AverageDegree ?AverageDegree . ?AverageDegree SNAMetric:hasValue ?valorAverageDegree . " + texto)

		if 'Component_less_than' in request.POST: #verifica se Degree_Centrality foi enviado na requisição
			Component_less_than = request.POST['Component_less_than']
			if Component_less_than:
				if  Component_less_than != "":
						texto = (""" FILTER( ?ValorComponent < """ + Component_less_than +") .")
						consulta+= (" ?rede SNAMetric:hasSNAMetricComponent ?Component . ?Component SNAMetric:hasValue ?ValorComponent . " + texto)

		if 'Component_greater_than' in request.POST: #verifica se Degree_Centrality foi enviado na requisição
			Component_greater_than = request.POST['Component_greater_than']
			if Component_greater_than:
				if  Component_greater_than != "":
						texto = (""" FILTER( ?ValorComponent > """ + Component_greater_than +") .")
						consulta+= (" ?rede SNAMetric:hasSNAMetricComponent ?Component . ?Component SNAMetric:hasValue ?ValorComponent . " + texto)

		if 'Density_less_than' in request.POST: #verifica se Degree_Centrality foi enviado na requisição
			Density_less_than = request.POST['Density_less_than']
			if Density_less_than:
				if  Density_less_than != "":
						texto = (""" FILTER( ?valorDensity < """ + Density_less_than +") .")
						consulta+= (" ?rede scnas:has_Density ?densidade . ?densidade SNAMetric:hasValue ?valorDensity . " + texto)

		if 'Density_greater_than' in request.POST: #verifica se Degree_Centrality foi enviado na requisição
			Density_greater_than = request.POST['Density_greater_than']
			if Density_greater_than:
				if  Density_greater_than != "":
						texto = (""" FILTER( ?valorDensity > """ + Density_greater_than +") .")
						consulta+= (" ?rede scnas:has_Density ?densidade . ?densidade SNAMetric:hasValue ?valorDensity . " + texto)

		if 'Periodic_Name' in request.POST: #verifica se Degree_Centrality foi enviado na requisição
			Periodic_Name = request.POST['Periodic_Name']
			if Periodic_Name:
				if  Periodic_Name != "":
						texto = ("""  ?type SNAMetric:hasName '""" + Periodic_Name +"' .")
						consulta+= (' ?assertion scnas:has_Type ?type .' + texto)			

		if 'Knowledge_Area_Name' in request.POST: #verifica se Degree_Centrality foi enviado na requisição
			Knowledge_Area_Name = request.POST['Knowledge_Area_Name']
			if Knowledge_Area_Name:
				if  Knowledge_Area_Name != "":
					texto = (""" ?KnowledgeArea SNAMetric:hasName '""" + Knowledge_Area_Name +"' .")							
					consulta += ("?type scnas:has_KnowledgeArea ?KnowledgeArea ." + texto	)	

		if 'Region' in request.POST: #verifica se Degree_Centrality foi enviado na requisição
 			Region = request.POST['Region']
 			if Region: 							
 				consulta += ("""
				?rede scnas:has_Location ?location .
 				?location SNAMetric:hasName ?NameLocation .""")
		if 'Degree_Centrality' in request.POST or 'Closeness_Centrality' in request.POST or 'Betweenness_Centrality' in request.POST:
			consulta+=(" ?assertion scnas:has_Network ?rede .")
			Actor= "Actor"
			consulta += ("""
					?rede scnas:has_Actor ?actor.
 					?actor SNAMetric:hasName ?nameActor .""")
			if 'Degree_Centrality' in request.POST: #verifica se Degree_Centrality foi enviado na requisição
	 			Degree_Centrality = request.POST['Degree_Centrality']
	 			if Degree_Centrality:
	 				Degree = "Degree Centrality " 							
	 				consulta += ("""
					?actor SNAMetric:hasSNAMetricDegreeCentrality ?DegreeCentrality .
					?DegreeCentrality SNAMetric:hasValue ?valueDC .""")
			if 'Closeness_Centrality' in request.POST: #verifica se Closeness_Centrality foi enviado na requisição
				Closeness_Centrality = request.POST['Closeness_Centrality']
				if Closeness_Centrality:
					Closeness = "Closeness Centrality "							
					consulta += ("""
					?actor SNAMetric:hasSNAMetricClosenessCentrality ?ClosenessCentrality .
					?ClosenessCentrality SNAMetric:hasValue ?valueCC .""")
			if 'Betweenness_Centrality' in request.POST: #verifica se Betweenness_Centrality foi enviado na requisição
				Betweenness_Centrality = request.POST['Betweenness_Centrality']
				if Betweenness_Centrality:
					Betweenness = "Betweenness Centrality "						
					consulta += ("""
					?actor SNAMetric:hasSNAMetricBetweennessCentrality ?BetweennessCentrality .
					?BetweennessCentrality SNAMetric:hasValue ?valueBC .""")
				
		if 'Density' in request.POST or 'Component' in request.POST or 	'Average_Degree' in request.POST or 'Actors_Number' in request.POST or 'Edges_Number' in request.POST:
			consulta+=(" ?assertion scnas:has_Network ?rede .")
			if 'Density' in request.POST: #verifica se Degree_Centrality foi enviado na requisição
				Density = request.POST['Density']
				if Density:
	 				Density_ = "Density"
	 				consulta += ("""
					?rede scnas:has_Density ?densidade .
		 			?densidade SNAMetric:hasValue ?valorDensity .""") 
			if 'Component' in request.POST: #verifica se Degree_Centrality foi enviado na requisição
	 			Component = request.POST['Component']
	 			if Component:
	 				consulta += ("""
					?rede SNAMetric:hasSNAMetricComponent ?Component .
	 				?Component SNAMetric:hasValue ?ValorComponent. """) 
			if 'Average_Degree' in request.POST: #verifica se Degree_Centrality foi enviado na requisição
	 			Average_Degree = request.POST['Average_Degree']
	 			if Average_Degree:
	 				consulta += ("""
					?rede scnas:has_AverageDegree ?AverageDegree .
					 ?AverageDegree SNAMetric:hasValue ?valorAverageDegree .""") 
			if 'Actors_Number' in request.POST: #verifica se Degree_Centrality foi enviado na requisição
	 			Actors_Number = request.POST['Actors_Number']
	 			if Actors_Number:
	 				consulta += ("""
					?rede scnas:has_ActorsNumber ?ActorsNumber .
	 				?ActorsNumber SNAMetric:hasValue ?ValueActorsNumber .""")
			if 'Edges_Number' in request.POST: #verifica se Degree_Centrality foi enviado na requisição
	 			Edges_Number = request.POST['Edges_Number']
	 			if Edges_Number:
	 				consulta += ("""
					?rede scnas:has_EdgesNumber ?EdgesNumber .
					?EdgesNumber SNAMetric:hasValue ?ValueEdgesNumber .""")


		consulta += ("""
		}
		LIMIT 10000""")

		sparql.setQuery(consulta)
		sparql.setReturnFormat(JSON)
		results = sparql.query().convert()
		
		listaTitulos= []

		def remove_repetidos(lista):
		    l = []
		    for i in lista:
		        if i not in l:
		            l.append(i)
		    l.sort()
		    return l

		for result in results["results"]["bindings"]:
			for var in results["head"]["vars"]:
				if var == "anoinicio":
					Inicio = "Inicio"
					listaAnoInicio.append(result[var]['value'])
				if var == "anofim":
					Fim = "Fim"
					listaAnoFim.append(result[var]['value'])	
				if var == "URL":
					DOI= "DOI"
					listaURL.append(result[var]['value'])
				if var == "NameLocation":
					Location = "Location"
					listaRegion.append(result[var]['value'])	
				if var == "NameAC":
					AC= "Knowledge Area"
					listaAC.append(result[var]['value'])
				if var == "title":
					Titles = "SCNAS"
					listaTitulos.append(result[var]['value'])
					aux= remove_repetidos(listaTitulos)
					counttitles= len(aux)	

				if 'Degree_Centrality' in request.POST or 'Closeness_Centrality' in request.POST or 'Betweenness_Centrality' in request.POST:
					if var == "nameActor":
						listaActor.append(result[var]['value'])
					if 'Degree_Centrality' in request.POST: #verifica se Degree_Centrality foi enviado na requisição
			 			Degree_Centrality = request.POST['Degree_Centrality']
			 			if Degree_Centrality:
			 				if var == "valueDC":
			 					listaDC.append(result[var]['value'])
					if 'Closeness_Centrality' in request.POST: #verifica se Closeness_Centrality foi enviado na requisição
						Closeness_Centrality = request.POST['Closeness_Centrality']
						if Closeness_Centrality:
							if var == "valueCC":
								listaCC.append(result[var]['value'])
					if 'Betweenness_Centrality' in request.POST: #verifica se Betweenness_Centrality foi enviado na requisição
						Betweenness_Centrality = request.POST['Betweenness_Centrality']
						if Betweenness_Centrality:
							if var == "valueBC":
								listaBC.append(result[var]['value'])
				if 'Density' in request.POST or 'Component' in request.POST or 'Average_Degree' in request.POST or 'Actors_Number' in request.POST or 'Edges_Number' in request.POST:
					if 'Density' in request.POST: #verifica se Betweenness_Centrality foi enviado na requisição
						Densidade= "Density"
						Density = request.POST['Density']
						if Density:
							if var == "valorDensity":
								listaDensity.append(result[var]['value'])
					if 'Component' in request.POST: #verifica se Betweenness_Centrality foi enviado na requisição
						Compo="Component"
						Component = request.POST['Component']
						if Component:
							if var == "ValorComponent":
								listaComponentes.append(result[var]['value'])
					if 'Average_Degree' in request.POST: #verifica se Betweenness_Centrality foi enviado na requisição
						Average_Degree = request.POST['Average_Degree']
						if Average_Degree:
							Average= "Average Degree"
							if var == "valorAverageDegree":
								listaAverageDegree.append(result[var]['value'])
					if 'Actors_Number' in request.POST: #verifica se Betweenness_Centrality foi enviado na requisição
						Actors_Number = request.POST['Actors_Number']
						if Actors_Number:
							AN= "Actors Number"
							if var == "ValueActorsNumber":
								listaActorsNumber.append(result[var]['value'])

					if 'Edges_Number' in request.POST: #verifica se Betweenness_Centrality foi enviado na requisição
						Edges_Number = request.POST['Edges_Number']
						if Edges_Number:
							EN= "Edges Number"
							if var == "ValueEdgesNumber":
								listaEdgesNumber.append(result[var]['value'])




	return render(request, "periodic.html", {'PeriodicOther':PeriodicOther, 'ActorMetrics': ActorMetrics, 'NetworkMetrics': NetworkMetrics, 'filtroKnowledgeArea':filtroKnowledgeArea, 'filtroNetworkMetrics': filtroNetworkMetrics, 'filtroActorsMetrics': filtroActorsMetrics, 'filtroPeriodic':filtroPeriodic, 'Atores': listaActor, 'DCs':listaDC, 'CCs':listaCC, 'BCs': listaBC, 'URLs': listaURL, 'Titulos': listaTitle, 'Densities': listaDensity, 'Componentes': listaComponentes, 'AverageDegrees': listaAverageDegree, "Regions": listaRegion, 
'Location': Location, 'Betweenness': Betweenness, 'Closeness': Closeness, 'Degree': Degree, 'DOI': DOI, 'Locations': ListaLocation, 'Actor': Actor, 'Densidade':Densidade, 'titulo': titulo, 'Compo':Compo, 'Averag': Average, 'numerodeatores': listaActorsNumber, 'AN':AN, 'EN':EN, "numerodeedges": listaEdgesNumber, "AC": AC, "listaAC": listaAC, 'listaTitles': listaTitulos, "Titles":Titles, "counttitles":counttitles, 'listaAnoFim':listaAnoFim, 'listaAnoInicio':listaAnoInicio,'Inicio':Inicio, 'Fim': Fim})


	
def Event(request):

	sparql = SPARQLWrapper("http://localhost:3030/SCNAS")
	consulta = ("""
prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#>
prefix owl: <http://www.w3.org/2002/07/owl#>
PREFIX xmlns:<http://www.nanopub.org/nschema>
PREFIX base:<http://www.nanopub.org/nschema>
PREFIX dc:<http://purl.org/dc/elements/1.1/>
PREFIX np:<http://www.nanopub.org/nschema#>
PREFIX ns:<http://www.w3.org/2003/06/sw-vocab-status/ns#>
PREFIX owl:<http://www.w3.org/2002/07/owl#>
PREFIX xml:<http://www.w3.org/XML/1998/namespace>
PREFIX foaf:<http://xmlns.com/foaf/0.1/>
PREFIX prov:<http://www.w3.org/ns/prov#>
PREFIX rdfg:<http://www.w3.org/2004/03/trix/rdfg-1/>
PREFIX skos:<http://www.w3.org/2004/02/skos/core#>
PREFIX time:<http://www.w3.org/2006/time#>
PREFIX fabio:<http://purl.org/spar/fabio/>
PREFIX terms:<http://purl.org/dc/terms/>
PREFIX datacite:<http://purl.org/spar/datacite/>
PREFIX SNAMetric:<http://ns.inria.fr/semsna/2009/06/21/SNAMetric#>
PREFIX XMLSchema:<http://www.w3.org/2000/10/XMLSchema#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX scnas:<http://www.semanticweb.org/cliente/ontologies/2019/9/SCNAS#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX sc: <http://purl.org/science/owl/sciencecommons/>

SELECT  *
WHERE{
 ?nanopublication np:hasAssertion ?assertion .
 ?nanopublication np:hasProvenance ?provenance .
 ?provenance datacite:usesIdentifierScheme ?DOI .
 ?DOI fabio:hasURL ?URL .
 ?provenance dc:title ?title .
 ?assertion rdf:type np:Assertion .
 ?assertion scnas:has_Type ?type .
 ?type rdf:type scnas:Event .

""")

	listaActor=[]
	listaDC= []
	listaCC= []
	listaBC= []
	listaURL= []
	listaTitulos= []
	listaRegion= []


	listaTitle= []
	listaDensity= []
	listaComponentes= []
	listaAverageDegree = []
	ListaLocation= []
	listaActorsNumber = []
	listaEdgesNumber= []
	listaAC = []
	aux=[]
	

	Location = "No"
	Betweenness = "No"
	Closeness = "No"
	Degree = "No"
	DOI = "No"
	#MÉTRICAS DE ATORES
	Actor="No"
	Densidade= "No"
	titulo = "No"
	Compo="No"
	Average= "No"
	AN= "No"
	EN= "No"
	AC= "No"
	Titles="No"
	counttitles=0

	Fim= "No"
	Inicio="No"
	listaAnoInicio=[]
	listaAnoFim=[]


	if request.method == "POST":

		if 'Network_Time' in request.POST: #verifica se Degree_Centrality foi enviado na requisição
			Network_Time = request.POST['Network_Time']
			if Network_Time:
				consulta+= ("""  ?assertion scnas:has_Network ?rede . 
				?rede scnas:has_Time ?tempo.
 				?tempo time:hasBeginning ?inicio .
 				?tempo time:hasEnd ?fim .
 				?inicio time:year ?anoinicio.
 				?fim time:year ?anofim .""" )

		if 'Knowledge_Area' in request.POST: #verifica se Degree_Centrality foi enviado na requisição
			Knowledge_Area = request.POST['Knowledge_Area']
			if Knowledge_Area:

				consulta+= (" ?type scnas:has_KnowledgeArea ?AC . ?AC SNAMetric:hasName ?NameAC . " )

		if 'Betweenness_Centrality_less_than' in request.POST: #verifica se Degree_Centrality foi enviado na requisição
			Betweenness_Centrality_less_than = request.POST['Betweenness_Centrality_less_than']
			if Betweenness_Centrality_less_than:
				if  Betweenness_Centrality_less_than != "":
						texto = (""" FILTER( ?valueBC < """ + Betweenness_Centrality_less_than +") .")
						consulta+= ("?actor SNAMetric:hasSNAMetricBetweennessCentrality ?BetweennessCentrality . ?BetweennessCentrality SNAMetric:hasValue ?valueBC ." + texto)

		if 'Betweenness_Centrality_greater_than' in request.POST: #verifica se Degree_Centrality foi enviado na requisição
			Betweenness_Centrality_greater_than = request.POST['Betweenness_Centrality_greater_than']
			if Betweenness_Centrality_greater_than:
				if  Betweenness_Centrality_greater_than != "":
						texto = (""" FILTER( ?valueBC > """ + Betweenness_Centrality_greater_than +") .")
						consulta+= ("?actor SNAMetric:hasSNAMetricBetweennessCentrality ?BetweennessCentrality . ?BetweennessCentrality SNAMetric:hasValue ?valueBC ." + texto)

		if 'Closeness_Centrality_less_than' in request.POST: #verifica se Degree_Centrality foi enviado na requisição
			Closeness_Centrality_less_than = request.POST['Closeness_Centrality_less_than']
			if Closeness_Centrality_less_than:
				if  Closeness_Centrality_less_than != "":
						texto = (""" FILTER( ?valueCC < """ + Closeness_Centrality_less_than +") .")
						consulta+= ("?actor SNAMetric:hasSNAMetricClosenessCentrality ?ClosenessCentrality . ?ClosenessCentrality SNAMetric:hasValue ?valueCC ." + texto)

		if 'Closeness_Centrality_greater_than' in request.POST: #verifica se Degree_Centrality foi enviado na requisição
			Closeness_Centrality_greater_than = request.POST['Closeness_Centrality_greater_than']
			if Closeness_Centrality_greater_than:
				if  Closeness_Centrality_greater_than != "":
						texto = (""" FILTER( ?valueCC > """ + Closeness_Centrality_greater_than +") .")
						consulta+= ("?actor SNAMetric:hasSNAMetricClosenessCentrality ?ClosenessCentrality . ?ClosenessCentrality SNAMetric:hasValue ?valueCC ." + texto)

		if 'Degree_Centrality_less_than' in request.POST: #verifica se Degree_Centrality foi enviado na requisição
			Degree_Centrality_less_than = request.POST['Degree_Centrality_less_than']
			if Degree_Centrality_less_than:
				if  Degree_Centrality_less_than != "":
						texto = (""" FILTER( ?valueDC < """ + Degree_Centrality_less_than +") .")
						consulta+= ("?actor SNAMetric:hasSNAMetricDegreeCentrality ?DegreeCentrality . ?DegreeCentrality SNAMetric:hasValue ?valueDC ." + texto)


		if 'Degree_Centrality_greater_than' in request.POST: #verifica se Degree_Centrality foi enviado na requisição
			Degree_Centrality_greater_than = request.POST['Degree_Centrality_greater_than']
			if Degree_Centrality_greater_than:
				if  Degree_Centrality_greater_than != "":
						texto = (""" FILTER( ?valueDC > """ + Degree_Centrality_greater_than +") .")
						consulta+= ("?actor SNAMetric:hasSNAMetricDegreeCentrality ?DegreeCentrality . ?DegreeCentrality SNAMetric:hasValue ?valueDC ." + texto)

		if 'Average_Degree_less_than' in request.POST: #verifica se Degree_Centrality foi enviado na requisição
			Average_Degree_less_than = request.POST['Average_Degree_less_than']
			if Average_Degree_less_than:
				if  Average_Degree_less_than != "":
						texto = (""" FILTER( ?valorAverageDegree < """ + Average_Degree_less_than +") .")
						consulta+= ("?rede scnas:has_AverageDegree ?AverageDegree . ?AverageDegree SNAMetric:hasValue ?valorAverageDegree ." + texto)

		if 'Average_Degree_less_than' in request.POST: #verifica se Degree_Centrality foi enviado na requisição
			Average_Degree_less_than = request.POST['Average_Degree_less_than']
			if Average_Degree_less_than:
				if  Average_Degree_less_than != "":
						texto = (""" FILTER( ?valorAverageDegree < """ + Average_Degree_less_than +") .")
						consulta+= ("?rede scnas:has_AverageDegree ?AverageDegree . ?AverageDegree SNAMetric:hasValue ?valorAverageDegree ." + texto)


		if 'Average_Degree_greater_than' in request.POST: #verifica se Degree_Centrality foi enviado na requisição
			Average_Degree_greater_than = request.POST['Average_Degree_greater_than']
			if Average_Degree_greater_than:
				if  Average_Degree_greater_than != "":
						texto = (""" FILTER( ?valorAverageDegree > """ + Average_Degree_greater_than +") .")
						consulta+= (" ?rede scnas:has_AverageDegree ?AverageDegree . ?AverageDegree SNAMetric:hasValue ?valorAverageDegree . " + texto)

		if 'Component_less_than' in request.POST: #verifica se Degree_Centrality foi enviado na requisição
			Component_less_than = request.POST['Component_less_than']
			if Component_less_than:
				if  Component_less_than != "":
						texto = (""" FILTER( ?ValorComponent < """ + Component_less_than +") .")
						consulta+= (" ?rede SNAMetric:hasSNAMetricComponent ?Component . ?Component SNAMetric:hasValue ?ValorComponent . " + texto)

		if 'Component_greater_than' in request.POST: #verifica se Degree_Centrality foi enviado na requisição
			Component_greater_than = request.POST['Component_greater_than']
			if Component_greater_than:
				if  Component_greater_than != "":
						texto = (""" FILTER( ?ValorComponent > """ + Component_greater_than +") .")
						consulta+= (" ?rede SNAMetric:hasSNAMetricComponent ?Component . ?Component SNAMetric:hasValue ?ValorComponent . " + texto)

		if 'Density_less_than' in request.POST: #verifica se Degree_Centrality foi enviado na requisição
			Density_less_than = request.POST['Density_less_than']
			if Density_less_than:
				if  Density_less_than != "":
						texto = (""" FILTER( ?valorDensity < """ + Density_less_than +") .")
						consulta+= (" ?rede scnas:has_Density ?densidade . ?densidade SNAMetric:hasValue ?valorDensity . " + texto)

		if 'Density_greater_than' in request.POST: #verifica se Degree_Centrality foi enviado na requisição
			Density_greater_than = request.POST['Density_greater_than']
			if Density_greater_than:
				if  Density_greater_than != "":
						texto = (""" FILTER( ?valorDensity > """ + Density_greater_than +") .")
						consulta+= (" ?rede scnas:has_Density ?densidade . ?densidade SNAMetric:hasValue ?valorDensity . " + texto)

		if 'Event_Name' in request.POST: #verifica se Degree_Centrality foi enviado na requisição
			Event_Name = request.POST['Event_Name']
			if Event_Name:
				if  Event_Name != "":
						texto = (""" ?type SNAMetric:hasName '""" + Event_Name +"' .")
						consulta+= ("  ?assertion scnas:has_Type ?type . " + texto)			

		if 'Knowledge_Area_Name' in request.POST: #verifica se Degree_Centrality foi enviado na requisição
			Knowledge_Area_Name = request.POST['Knowledge_Area_Name']
			if Knowledge_Area_Name:
				if  Knowledge_Area_Name != "":
					texto = (""" ?KnowledgeArea SNAMetric:hasName '""" + Knowledge_Area_Name +"' .")							
					consulta += ("?type scnas:has_KnowledgeArea ?KnowledgeArea ." + texto	)	

		if 'Region' in request.POST: #verifica se Degree_Centrality foi enviado na requisição
 			Region = request.POST['Region']
 			if Region: 							
 				consulta += ("""
				?rede scnas:has_Location ?location .
 				?location SNAMetric:hasName ?NameLocation .""")
		if 'Degree_Centrality' in request.POST or 'Closeness_Centrality' in request.POST or 'Betweenness_Centrality' in request.POST:
			consulta+=(" ?assertion scnas:has_Network ?rede .")		
			Actor= "Actor"
			consulta += ("""
					?rede scnas:has_Actor ?actor.
 					?actor SNAMetric:hasName ?nameActor .""")
			if 'Degree_Centrality' in request.POST: #verifica se Degree_Centrality foi enviado na requisição
	 			Degree_Centrality = request.POST['Degree_Centrality']
	 			if Degree_Centrality:
	 				Degree = "Degree Centrality " 							
	 				consulta += ("""
					?actor SNAMetric:hasSNAMetricDegreeCentrality ?DegreeCentrality .
					?DegreeCentrality SNAMetric:hasValue ?valueDC .""")
			if 'Closeness_Centrality' in request.POST: #verifica se Closeness_Centrality foi enviado na requisição
				Closeness_Centrality = request.POST['Closeness_Centrality']
				if Closeness_Centrality:
					Closeness = "Closeness Centrality "							
					consulta += ("""
					?actor SNAMetric:hasSNAMetricClosenessCentrality ?ClosenessCentrality .
					?ClosenessCentrality SNAMetric:hasValue ?valueCC .""")
			if 'Betweenness_Centrality' in request.POST: #verifica se Betweenness_Centrality foi enviado na requisição
				Betweenness_Centrality = request.POST['Betweenness_Centrality']
				if Betweenness_Centrality:
					Betweenness = "Betweenness Centrality "						
					consulta += ("""
					?actor SNAMetric:hasSNAMetricBetweennessCentrality ?BetweennessCentrality .
					?BetweennessCentrality SNAMetric:hasValue ?valueBC .""")
		if 'Density' in request.POST or 'Component' in request.POST or 	'Average_Degree' in request.POST or 'Actors_Number' in request.POST or 'Edges_Number' in request.POST:
			consulta+=(" ?assertion scnas:has_Network ?rede .")		
			if 'Density' in request.POST: #verifica se Degree_Centrality foi enviado na requisição
	 			Density = request.POST['Density']
	 			if Density:
	 				Density_ = "Density"
	 				consulta += ("""
					?rede scnas:has_Density ?densidade .
		 			?densidade SNAMetric:hasValue ?valorDensity .""") 
			if 'Component' in request.POST: #verifica se Degree_Centrality foi enviado na requisição
	 			Component = request.POST['Component']
	 			if Component:
	 				consulta += ("""
					?rede SNAMetric:hasSNAMetricComponent ?Component .
	 				?Component SNAMetric:hasValue ?ValorComponent. """) 
			if 'Average_Degree' in request.POST: #verifica se Degree_Centrality foi enviado na requisição
	 			Average_Degree = request.POST['Average_Degree']
	 			if Average_Degree:
	 				consulta += ("""
					?rede scnas:has_AverageDegree ?AverageDegree .
					 ?AverageDegree SNAMetric:hasValue ?valorAverageDegree .""") 
			if 'Actors_Number' in request.POST: #verifica se Degree_Centrality foi enviado na requisição
	 			Actors_Number = request.POST['Actors_Number']
	 			if Actors_Number:
	 				consulta += ("""
					?rede scnas:has_ActorsNumber ?ActorsNumber .
	 				?ActorsNumber SNAMetric:hasValue ?ValueActorsNumber .""")
			if 'Edges_Number' in request.POST: #verifica se Degree_Centrality foi enviado na requisição
	 			Edges_Number = request.POST['Edges_Number']
	 			if Edges_Number:
	 				consulta += ("""
					?rede scnas:has_EdgesNumber ?EdgesNumber .
					?EdgesNumber SNAMetric:hasValue ?ValueEdgesNumber .""")


		consulta += ("""
		}
		LIMIT 10000""")

		sparql.setQuery(consulta)
		sparql.setReturnFormat(JSON)
		results = sparql.query().convert()
		
		def remove_repetidos(lista):
		    l = []
		    for i in lista:
		        if i not in l:
		            l.append(i)
		    l.sort()
		    return l

		for result in results["results"]["bindings"]:
			for var in results["head"]["vars"]:
				if var == "anoinicio":
					Inicio = "Inicio"
					listaAnoInicio.append(result[var]['value'])
				if var == "anofim":
					Fim = "Fim"
					listaAnoFim.append(result[var]['value'])	
				if var == "URL":
					DOI= "DOI"
					listaURL.append(result[var]['value'])
				if var == "NameLocation":
					Location = "Location"
					listaRegion.append(result[var]['value'])
				if var == "NameAC":
					AC= "Knowledge Area"
					listaAC.append(result[var]['value'])
				if var == "title":
					Titles = "SCNAS"
					listaTitulos.append(result[var]['value'])
					aux= remove_repetidos(listaTitulos)
					counttitles= len(aux)			
				if 'Degree_Centrality' in request.POST or 'Closeness_Centrality' in request.POST or 'Betweenness_Centrality' in request.POST:
					if var == "nameActor":
						listaActor.append(result[var]['value'])
					if 'Degree_Centrality' in request.POST: #verifica se Degree_Centrality foi enviado na requisição
			 			Degree_Centrality = request.POST['Degree_Centrality']
			 			if Degree_Centrality:
			 				if var == "valueDC":
			 					listaDC.append(result[var]['value'])
					if 'Closeness_Centrality' in request.POST: #verifica se Closeness_Centrality foi enviado na requisição
						Closeness_Centrality = request.POST['Closeness_Centrality']
						if Closeness_Centrality:
							if var == "valueCC":
								listaCC.append(result[var]['value'])
					if 'Betweenness_Centrality' in request.POST: #verifica se Betweenness_Centrality foi enviado na requisição
						Betweenness_Centrality = request.POST['Betweenness_Centrality']
						if Betweenness_Centrality:
							if var == "valueBC":
								listaBC.append(result[var]['value'])
				if 'Density' in request.POST or 'Component' in request.POST or 'Average_Degree' in request.POST or 'Actors_Number' in request.POST or 'Edges_Number' in request.POST:
					if 'Density' in request.POST: #verifica se Betweenness_Centrality foi enviado na requisição
						Densidade= "Density"
						Density = request.POST['Density']
						if Density:
							if var == "valorDensity":
								listaDensity.append(result[var]['value'])
					if 'Component' in request.POST: #verifica se Betweenness_Centrality foi enviado na requisição
						Compo="Component"
						Component = request.POST['Component']
						if Component:
							if var == "ValorComponent":
								listaComponentes.append(result[var]['value'])
					if 'Average_Degree' in request.POST: #verifica se Betweenness_Centrality foi enviado na requisição
						Average_Degree = request.POST['Average_Degree']
						if Average_Degree:
							Average= "Average Degree"
							if var == "valorAverageDegree":
								listaAverageDegree.append(result[var]['value'])
					if 'Actors_Number' in request.POST: #verifica se Betweenness_Centrality foi enviado na requisição
						Actors_Number = request.POST['Actors_Number']
						if Actors_Number:
							AN= "Actors Number"
							if var == "ValueActorsNumber":
								listaActorsNumber.append(result[var]['value'])

					if 'Edges_Number' in request.POST: #verifica se Betweenness_Centrality foi enviado na requisição
						Edges_Number = request.POST['Edges_Number']
						if Edges_Number:
							EN= "Edges Number"
							if var == "ValueEdgesNumber":
								listaEdgesNumber.append(result[var]['value'])


	print(listaAC)

	return render(request, "Event.html", {'EventOther':EventOther, 'filtroEvent':filtroEvent, 'ActorMetrics': ActorMetrics, 'NetworkMetrics': NetworkMetrics, 'filtroKnowledgeArea':filtroKnowledgeArea, 'filtroNetworkMetrics': filtroNetworkMetrics, 'filtroActorsMetrics': filtroActorsMetrics, 'filtroPeriodic':filtroPeriodic, 'Atores': listaActor, 'DCs':listaDC, 'CCs':listaCC, 'BCs': listaBC, 'URLs': listaURL, 'Titulos': listaTitle, 'Densities': listaDensity, 'Componentes': listaComponentes, 'AverageDegrees': listaAverageDegree, "Regions": listaRegion, 
'Location': Location, 'Betweenness': Betweenness, 'Closeness': Closeness, 'Degree': Degree, 'DOI': DOI, 'Locations': ListaLocation, 'Actor': Actor, 'Densidade':Densidade, 'titulo': titulo, 'Compo':Compo, 'Averag': Average, 'numerodeatores': listaActorsNumber, 'AN':AN, 'EN':EN, "numerodeedges": listaEdgesNumber, "listaAC": listaAC, "AC": AC, 'listaTitles': listaTitulos, "Titles":Titles, 'counttitles':counttitles, 'listaAnoFim':listaAnoFim, 'listaAnoInicio':listaAnoInicio,'Inicio':Inicio, 'Fim': Fim})


def PGP(request):

	sparql = SPARQLWrapper("http://localhost:3030/SCNAS")
	consulta = ("""
prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#>
prefix owl: <http://www.w3.org/2002/07/owl#>
PREFIX xmlns:<http://www.nanopub.org/nschema>
PREFIX base:<http://www.nanopub.org/nschema>
PREFIX dc:<http://purl.org/dc/elements/1.1/>
PREFIX np:<http://www.nanopub.org/nschema#>
PREFIX ns:<http://www.w3.org/2003/06/sw-vocab-status/ns#>
PREFIX owl:<http://www.w3.org/2002/07/owl#>
PREFIX xml:<http://www.w3.org/XML/1998/namespace>
PREFIX foaf:<http://xmlns.com/foaf/0.1/>
PREFIX prov:<http://www.w3.org/ns/prov#>
PREFIX rdfg:<http://www.w3.org/2004/03/trix/rdfg-1/>
PREFIX skos:<http://www.w3.org/2004/02/skos/core#>
PREFIX time:<http://www.w3.org/2006/time#>
PREFIX fabio:<http://purl.org/spar/fabio/>
PREFIX terms:<http://purl.org/dc/terms/>
PREFIX datacite:<http://purl.org/spar/datacite/>
PREFIX SNAMetric:<http://ns.inria.fr/semsna/2009/06/21/SNAMetric#>
PREFIX XMLSchema:<http://www.w3.org/2000/10/XMLSchema#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX scnas:<http://www.semanticweb.org/cliente/ontologies/2019/9/SCNAS#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX sc: <http://purl.org/science/owl/sciencecommons/>

SELECT  *
WHERE{
 ?nanopublication np:hasAssertion ?assertion .
 ?nanopublication np:hasProvenance ?provenance .
 ?provenance datacite:usesIdentifierScheme ?DOI .
 ?DOI fabio:hasURL ?URL .
 ?provenance dc:title ?title .
 ?assertion rdf:type np:Assertion .
 ?assertion scnas:has_Type ?type .
 ?type rdf:type scnas:Postgraduate_Programmes .

""")

	listaActor=[]
	listaDC= []
	listaCC= []
	listaBC= []
	listaURL= []
	listaTitulos= []
	listaRegion= []
	aux=[]


	listaTitle= []
	listaDensity= []
	listaComponentes= []
	listaAverageDegree = []
	ListaLocation= []
	listaActorsNumber = []
	listaEdgesNumber= []		
	listaAC=[]
	listaHEI=[]



	Location = "No"
	Betweenness = "No"
	Closeness = "No"
	Degree = "No"
	DOI = "No"
	#MÉTRICAS DE ATORES
	Actor="No"
	Densidade= "No"
	titulo = "No"
	Compo="No"
	Average= "No"
	AN= "No"
	EN= "No"
	Titles="No"
	AC="No"
	HEIInstitution="No"
	counttitles = 0

	Fim= "No"
	Inicio="No"
	listaAnoInicio=[]
	listaAnoFim=[]



	if request.method == "POST":

		if 'Network_Time' in request.POST: #verifica se Degree_Centrality foi enviado na requisição
			Network_Time = request.POST['Network_Time']
			if Network_Time:
				consulta+= ("""  ?assertion scnas:has_Network ?rede . 
				?rede scnas:has_Time ?tempo.
 				?tempo time:hasBeginning ?inicio .
 				?tempo time:hasEnd ?fim .
 				?inicio time:year ?anoinicio.
 				?fim time:year ?anofim .""" )

		if 'HEI' in request.POST: #verifica se Degree_Centrality foi enviado na requisição
			HEI = request.POST['HEI']
			if HEI:
				consulta+= ("  ?type scnas:has_HEI ?HEI . ?HEI SNAMetric:hasName ?nomeHEI.  " )

		if 'Knowledge_Area' in request.POST: #verifica se Degree_Centrality foi enviado na requisição
			Knowledge_Area = request.POST['Knowledge_Area']
			if Knowledge_Area:

				consulta+= (" ?type scnas:has_KnowledgeArea ?AC . ?AC SNAMetric:hasName ?NameAC . " )

		if 'Betweenness_Centrality_less_than' in request.POST: #verifica se Degree_Centrality foi enviado na requisição
			Betweenness_Centrality_less_than = request.POST['Betweenness_Centrality_less_than']
			if Betweenness_Centrality_less_than:
				if  Betweenness_Centrality_less_than != "":
						texto = (""" FILTER( ?valueBC < """ + Betweenness_Centrality_less_than +") .")
						consulta+= ("?actor SNAMetric:hasSNAMetricBetweennessCentrality ?BetweennessCentrality . ?BetweennessCentrality SNAMetric:hasValue ?valueBC ." + texto)

		if 'Betweenness_Centrality_greater_than' in request.POST: #verifica se Degree_Centrality foi enviado na requisição
			Betweenness_Centrality_greater_than = request.POST['Betweenness_Centrality_greater_than']
			if Betweenness_Centrality_greater_than:
				if  Betweenness_Centrality_greater_than != "":
						texto = (""" FILTER( ?valueBC > """ + Betweenness_Centrality_greater_than +") .")
						consulta+= ("?actor SNAMetric:hasSNAMetricBetweennessCentrality ?BetweennessCentrality . ?BetweennessCentrality SNAMetric:hasValue ?valueBC ." + texto)

		if 'Closeness_Centrality_less_than' in request.POST: #verifica se Degree_Centrality foi enviado na requisição
			Closeness_Centrality_less_than = request.POST['Closeness_Centrality_less_than']
			if Closeness_Centrality_less_than:
				if  Closeness_Centrality_less_than != "":
						texto = (""" FILTER( ?valueCC < """ + Closeness_Centrality_less_than +") .")
						consulta+= ("?actor SNAMetric:hasSNAMetricClosenessCentrality ?ClosenessCentrality . ?ClosenessCentrality SNAMetric:hasValue ?valueCC ." + texto)

		if 'Closeness_Centrality_greater_than' in request.POST: #verifica se Degree_Centrality foi enviado na requisição
			Closeness_Centrality_greater_than = request.POST['Closeness_Centrality_greater_than']
			if Closeness_Centrality_greater_than:
				if  Closeness_Centrality_greater_than != "":
						texto = (""" FILTER( ?valueCC > """ + Closeness_Centrality_greater_than +") .")
						consulta+= ("?actor SNAMetric:hasSNAMetricClosenessCentrality ?ClosenessCentrality . ?ClosenessCentrality SNAMetric:hasValue ?valueCC ." + texto)

		if 'Degree_Centrality_less_than' in request.POST: #verifica se Degree_Centrality foi enviado na requisição
			Degree_Centrality_less_than = request.POST['Degree_Centrality_less_than']
			if Degree_Centrality_less_than:
				if  Degree_Centrality_less_than != "":
						texto = (""" FILTER( ?valueDC < """ + Degree_Centrality_less_than +") .")
						consulta+= ("?actor SNAMetric:hasSNAMetricDegreeCentrality ?DegreeCentrality . ?DegreeCentrality SNAMetric:hasValue ?valueDC ." + texto)


		if 'Degree_Centrality_greater_than' in request.POST: #verifica se Degree_Centrality foi enviado na requisição
			Degree_Centrality_greater_than = request.POST['Degree_Centrality_greater_than']
			if Degree_Centrality_greater_than:
				if  Degree_Centrality_greater_than != "":
						texto = (""" FILTER( ?valueDC > """ + Degree_Centrality_greater_than +") .")
						consulta+= ("?actor SNAMetric:hasSNAMetricDegreeCentrality ?DegreeCentrality . ?DegreeCentrality SNAMetric:hasValue ?valueDC ." + texto)

		if 'Average_Degree_less_than' in request.POST: #verifica se Degree_Centrality foi enviado na requisição
			Average_Degree_less_than = request.POST['Average_Degree_less_than']
			if Average_Degree_less_than:
				if  Average_Degree_less_than != "":
						texto = (""" FILTER( ?valorAverageDegree < """ + Average_Degree_less_than +") .")
						consulta+= ("?rede scnas:has_AverageDegree ?AverageDegree . ?AverageDegree SNAMetric:hasValue ?valorAverageDegree ." + texto)

		if 'Average_Degree_less_than' in request.POST: #verifica se Degree_Centrality foi enviado na requisição
			Average_Degree_less_than = request.POST['Average_Degree_less_than']
			if Average_Degree_less_than:
				if  Average_Degree_less_than != "":
						texto = (""" FILTER( ?valorAverageDegree < """ + Average_Degree_less_than +") .")
						consulta+= ("?rede scnas:has_AverageDegree ?AverageDegree . ?AverageDegree SNAMetric:hasValue ?valorAverageDegree ." + texto)


		if 'Average_Degree_greater_than' in request.POST: #verifica se Degree_Centrality foi enviado na requisição
			Average_Degree_greater_than = request.POST['Average_Degree_greater_than']
			if Average_Degree_greater_than:
				if  Average_Degree_greater_than != "":
						texto = (""" FILTER( ?valorAverageDegree > """ + Average_Degree_greater_than +") .")
						consulta+= (" ?rede scnas:has_AverageDegree ?AverageDegree . ?AverageDegree SNAMetric:hasValue ?valorAverageDegree . " + texto)

		if 'Component_less_than' in request.POST: #verifica se Degree_Centrality foi enviado na requisição
			Component_less_than = request.POST['Component_less_than']
			if Component_less_than:
				if  Component_less_than != "":
						texto = (""" FILTER( ?ValorComponent < """ + Component_less_than +") .")
						consulta+= (" ?rede SNAMetric:hasSNAMetricComponent ?Component . ?Component SNAMetric:hasValue ?ValorComponent . " + texto)

		if 'Component_greater_than' in request.POST: #verifica se Degree_Centrality foi enviado na requisição
			Component_greater_than = request.POST['Component_greater_than']
			if Component_greater_than:
				if  Component_greater_than != "":
						texto = (""" FILTER( ?ValorComponent > """ + Component_greater_than +") .")
						consulta+= (" ?rede SNAMetric:hasSNAMetricComponent ?Component . ?Component SNAMetric:hasValue ?ValorComponent . " + texto)

		if 'Density_less_than' in request.POST: #verifica se Degree_Centrality foi enviado na requisição
			Density_less_than = request.POST['Density_less_than']
			if Density_less_than:
				if  Density_less_than != "":
						texto = (""" FILTER( ?valorDensity < """ + Density_less_than +") .")
						consulta+= (" ?rede scnas:has_Density ?densidade . ?densidade SNAMetric:hasValue ?valorDensity . " + texto)

		if 'Density_greater_than' in request.POST: #verifica se Degree_Centrality foi enviado na requisição
			Density_greater_than = request.POST['Density_greater_than']
			if Density_greater_than:
				if  Density_greater_than != "":
						texto = (""" FILTER( ?valorDensity > """ + Density_greater_than +") .")
						consulta+= (" ?rede scnas:has_Density ?densidade . ?densidade SNAMetric:hasValue ?valorDensity . " + texto)

		if 'Event_Name' in request.POST: #verifica se Degree_Centrality foi enviado na requisição
			Event_Name = request.POST['Event_Name']
			if Event_Name:
				if  Event_Name != "":
						texto = (""" ?type SNAMetric:hasName '""" + Event_Name +"' .")
						consulta+= ("  ?assertion scnas:has_Type ?type . " + texto)			

		if 'Knowledge_Area_Name' in request.POST: #verifica se Degree_Centrality foi enviado na requisição
			Knowledge_Area_Name = request.POST['Knowledge_Area_Name']
			if Knowledge_Area_Name:
				if  Knowledge_Area_Name != "":
					texto = (""" ?KnowledgeArea SNAMetric:hasName '""" + Knowledge_Area_Name +"' .")							
					consulta += ("?type scnas:has_KnowledgeArea ?KnowledgeArea ." + texto	)	

		if 'Region' in request.POST: #verifica se Degree_Centrality foi enviado na requisição
 			Region = request.POST['Region']
 			if Region: 							
 				consulta += ("""
				?rede scnas:has_Location ?location .
 				?location SNAMetric:hasName ?NameLocation .""")
		if 'Degree_Centrality' in request.POST or 'Closeness_Centrality' in request.POST or 'Betweenness_Centrality' in request.POST:
			consulta+=(" ?assertion scnas:has_Network ?rede .")	
			Actor= "Actor"
			consulta += ("""
					?rede scnas:has_Actor ?actor.
 					?actor SNAMetric:hasName ?nameActor .""")
			if 'Degree_Centrality' in request.POST: #verifica se Degree_Centrality foi enviado na requisição
	 			Degree_Centrality = request.POST['Degree_Centrality']
	 			if Degree_Centrality:
	 				Degree = "Degree Centrality " 							
	 				consulta += ("""
					?actor SNAMetric:hasSNAMetricDegreeCentrality ?DegreeCentrality .
					?DegreeCentrality SNAMetric:hasValue ?valueDC .""")
			if 'Closeness_Centrality' in request.POST: #verifica se Closeness_Centrality foi enviado na requisição
				Closeness_Centrality = request.POST['Closeness_Centrality']
				if Closeness_Centrality:
					Closeness = "Closeness Centrality "							
					consulta += ("""
					?actor SNAMetric:hasSNAMetricClosenessCentrality ?ClosenessCentrality .
					?ClosenessCentrality SNAMetric:hasValue ?valueCC .""")
			if 'Betweenness_Centrality' in request.POST: #verifica se Betweenness_Centrality foi enviado na requisição
				Betweenness_Centrality = request.POST['Betweenness_Centrality']
				if Betweenness_Centrality:
					Betweenness = "Betweenness Centrality "						
					consulta += ("""
					?actor SNAMetric:hasSNAMetricBetweennessCentrality ?BetweennessCentrality .
					?BetweennessCentrality SNAMetric:hasValue ?valueBC .""")
				
		if 'Density' in request.POST or 'Component' in request.POST or 	'Average_Degree' in request.POST or 'Actors_Number' in request.POST or 'Edges_Number' in request.POST:
			consulta+=(" ?assertion scnas:has_Network ?rede .")	
			if 'Density' in request.POST: #verifica se Degree_Centrality foi enviado na requisição
	 			Density = request.POST['Density']
	 			if Density:
	 				Density_ = "Density"
	 				consulta += ("""
					?rede scnas:has_Density ?densidade .
		 			?densidade SNAMetric:hasValue ?valorDensity .""") 
			if 'Component' in request.POST: #verifica se Degree_Centrality foi enviado na requisição
	 			Component = request.POST['Component']
	 			if Component:
	 				consulta += ("""
					?rede SNAMetric:hasSNAMetricComponent ?Component .
	 				?Component SNAMetric:hasValue ?ValorComponent. """) 
			if 'Average_Degree' in request.POST: #verifica se Degree_Centrality foi enviado na requisição
	 			Average_Degree = request.POST['Average_Degree']
	 			if Average_Degree:
	 				consulta += ("""
					?rede scnas:has_AverageDegree ?AverageDegree .
					 ?AverageDegree SNAMetric:hasValue ?valorAverageDegree .""") 
			if 'Actors_Number' in request.POST: #verifica se Degree_Centrality foi enviado na requisição
	 			Actors_Number = request.POST['Actors_Number']
	 			if Actors_Number:
	 				consulta += ("""
					?rede scnas:has_ActorsNumber ?ActorsNumber .
	 				?ActorsNumber SNAMetric:hasValue ?ValueActorsNumber .""")
			if 'Edges_Number' in request.POST: #verifica se Degree_Centrality foi enviado na requisição
	 			Edges_Number = request.POST['Edges_Number']
	 			if Edges_Number:
	 				consulta += ("""
					?rede scnas:has_EdgesNumber ?EdgesNumber .
					?EdgesNumber SNAMetric:hasValue ?ValueEdgesNumber .""")


		consulta += ("""
		}
		LIMIT 10000""")

		sparql.setQuery(consulta)
		sparql.setReturnFormat(JSON)
		results = sparql.query().convert()

		def remove_repetidos(lista):
		    l = []
		    for i in lista:
		        if i not in l:
		            l.append(i)
		    l.sort()
		    return l

		for result in results["results"]["bindings"]:
			for var in results["head"]["vars"]:
				if var == "anoinicio":
					Inicio = "Inicio"
					listaAnoInicio.append(result[var]['value'])
				if var == "anofim":
					Fim = "Fim"
					listaAnoFim.append(result[var]['value'])
				if var == "nomeHEI":
					HEIInstitution= "Institution"
					listaHEI.append(result[var]['value'])
				if var == "NameAC":
					AC= "Knowledge Area"
					listaAC.append(result[var]['value'])
				if var == "URL":
					DOI= "DOI"
					listaURL.append(result[var]['value'])
				if var == "NameLocation":
					Location = "Location"
					listaRegion.append(result[var]['value'])
				if var == "title":
					Titles = "SCNAS"
					listaTitulos.append(result[var]['value'])
					aux= remove_repetidos(listaTitulos)
					counttitles= len(aux)					
				if 'Degree_Centrality' in request.POST or 'Closeness_Centrality' in request.POST or 'Betweenness_Centrality' in request.POST:		
					if var == "nameActor":
						listaActor.append(result[var]['value'])
					if 'Degree_Centrality' in request.POST: #verifica se Degree_Centrality foi enviado na requisição
			 			Degree_Centrality = request.POST['Degree_Centrality']
			 			if Degree_Centrality:
			 				if var == "valueDC":
			 					listaDC.append(result[var]['value'])
					if 'Closeness_Centrality' in request.POST: #verifica se Closeness_Centrality foi enviado na requisição
						Closeness_Centrality = request.POST['Closeness_Centrality']
						if Closeness_Centrality:
							if var == "valueCC":
								listaCC.append(result[var]['value'])
					if 'Betweenness_Centrality' in request.POST: #verifica se Betweenness_Centrality foi enviado na requisição
						Betweenness_Centrality = request.POST['Betweenness_Centrality']
						if Betweenness_Centrality:
							if var == "valueBC":
								listaBC.append(result[var]['value'])
				if 'Density' in request.POST or 'Component' in request.POST or 'Average_Degree' in request.POST or 'Actors_Number' in request.POST or 'Edges_Number' in request.POST:
					if 'Density' in request.POST: #verifica se Betweenness_Centrality foi enviado na requisição
						Densidade= "Density"
						Density = request.POST['Density']
						if Density:
							if var == "valorDensity":
								listaDensity.append(result[var]['value'])
					if 'Component' in request.POST: #verifica se Betweenness_Centrality foi enviado na requisição
						Compo="Component"
						Component = request.POST['Component']
						if Component:
							if var == "ValorComponent":
								listaComponentes.append(result[var]['value'])
					if 'Average_Degree' in request.POST: #verifica se Betweenness_Centrality foi enviado na requisição
						Average_Degree = request.POST['Average_Degree']
						if Average_Degree:
							Average= "Average Degree"
							if var == "valorAverageDegree":
								listaAverageDegree.append(result[var]['value'])
					if 'Actors_Number' in request.POST: #verifica se Betweenness_Centrality foi enviado na requisição
						Actors_Number = request.POST['Actors_Number']
						if Actors_Number:
							AN= "Actors Number"
							if var == "ValueActorsNumber":
								listaActorsNumber.append(result[var]['value'])

					if 'Edges_Number' in request.POST: #verifica se Betweenness_Centrality foi enviado na requisição
						Edges_Number = request.POST['Edges_Number']
						if Edges_Number:
							EN= "Edges Number"
							if var == "ValueEdgesNumber":
								listaEdgesNumber.append(result[var]['value'])


	return render(request, "pgp.html", {'PGPOther':PGPOther, 'filtroInstitution':filtroInstitution, 'ActorMetrics': ActorMetrics, 'NetworkMetrics': NetworkMetrics, 'filtroKnowledgeArea':filtroKnowledgeArea, 'filtroNetworkMetrics': filtroNetworkMetrics, 'filtroActorsMetrics': filtroActorsMetrics, 'filtroPeriodic':filtroPeriodic, 'Atores': listaActor, 'DCs':listaDC, 'CCs':listaCC, 'BCs': listaBC, 'URLs': listaURL, 'Titulos': listaTitle, 'Densities': listaDensity, 'Componentes': listaComponentes, 'AverageDegrees': listaAverageDegree, "Regions": listaRegion, 
'Location': Location, 'Betweenness': Betweenness, 'Closeness': Closeness, 'Degree': Degree, 'DOI': DOI, 'Locations': ListaLocation, 'Actor': Actor, 'Densidade':Densidade, 'titulo': titulo, 'Compo':Compo, 'Averag': Average, 'numerodeatores': listaActorsNumber, 'AN':AN, 'EN':EN, "numerodeedges": listaEdgesNumber,'listaTitles': listaTitulos, "Titles":Titles, 'counttitles':counttitles, "listaAC": listaAC, "AC": AC, 'HEIInstitution': HEIInstitution, 'listaHEI':listaHEI, 'listaAnoFim':listaAnoFim, 'listaAnoInicio':listaAnoInicio,'Inicio':Inicio, 'Fim': Fim})



def HEI(request):

	sparql = SPARQLWrapper("http://localhost:3030/SCNAS")
	consulta = ("""
prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#>
prefix owl: <http://www.w3.org/2002/07/owl#>
PREFIX xmlns:<http://www.nanopub.org/nschema>
PREFIX base:<http://www.nanopub.org/nschema>
PREFIX dc:<http://purl.org/dc/elements/1.1/>
PREFIX np:<http://www.nanopub.org/nschema#>
PREFIX ns:<http://www.w3.org/2003/06/sw-vocab-status/ns#>
PREFIX owl:<http://www.w3.org/2002/07/owl#>
PREFIX xml:<http://www.w3.org/XML/1998/namespace>
PREFIX foaf:<http://xmlns.com/foaf/0.1/>
PREFIX prov:<http://www.w3.org/ns/prov#>
PREFIX rdfg:<http://www.w3.org/2004/03/trix/rdfg-1/>
PREFIX skos:<http://www.w3.org/2004/02/skos/core#>
PREFIX time:<http://www.w3.org/2006/time#>
PREFIX fabio:<http://purl.org/spar/fabio/>
PREFIX terms:<http://purl.org/dc/terms/>
PREFIX datacite:<http://purl.org/spar/datacite/>
PREFIX SNAMetric:<http://ns.inria.fr/semsna/2009/06/21/SNAMetric#>
PREFIX XMLSchema:<http://www.w3.org/2000/10/XMLSchema#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX scnas:<http://www.semanticweb.org/cliente/ontologies/2019/9/SCNAS#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX sc: <http://purl.org/science/owl/sciencecommons/>

SELECT  *
WHERE{
 ?nanopublication np:hasAssertion ?assertion .
 ?nanopublication np:hasProvenance ?provenance .
 ?provenance datacite:usesIdentifierScheme ?DOI .
 ?DOI fabio:hasURL ?URL .
 ?provenance dc:title ?title .
 ?assertion rdf:type np:Assertion .
 ?assertion scnas:has_Type ?type .
 ?type rdf:type scnas:High_Education_Institution.

""")

	listaActor=[]
	listaDC= []
	listaCC= []
	listaBC= []
	listaURL= []
	listaTitulos= []


	listaTitle= []
	listaDensity= []
	listaComponentes= []
	listaAverageDegree = []
	ListaLocation= []
	listaActorsNumber = []
	listaEdgesNumber= []
	listaInstitution=[]
	listaRegion=[]
	aux=[]

	Institution="No"
	Location = "No"
	Betweenness = "No"
	Closeness = "No"
	Degree = "No"
	DOI = "No"
	#MÉTRICAS DE ATORES
	Actor="No"
	Densidade= "No"
	titulo = "No"
	Compo="No"
	Average= "No"
	AN= "No"
	EN= "No"
	Titles="No"
	counttitles=0

	Fim= "No"
	Inicio="No"
	listaAnoInicio=[]
	listaAnoFim=[]


	if request.method == "POST":

		if 'Network_Time' in request.POST: #verifica se Degree_Centrality foi enviado na requisição
			Network_Time = request.POST['Network_Time']
			if Network_Time:
				consulta+= ("""  ?assertion scnas:has_Network ?rede . 
				?rede scnas:has_Time ?tempo.
 				?tempo time:hasBeginning ?inicio .
 				?tempo time:hasEnd ?fim .
 				?inicio time:year ?anoinicio.
 				?fim time:year ?anofim .""" )


		if 'Region' in request.POST: #verifica se Degree_Centrality foi enviado na requisição
			Region = request.POST['Region']
			if Region:
				consulta+= ("  ?type scnas:has_Location ?Location .  ?Location SNAMetric:hasName ?nameLocation ." )


		if 'High_Education_Institution' in request.POST: #verifica se Degree_Centrality foi enviado na requisição
			High_Education_Institution = request.POST['High_Education_Institution']
			if High_Education_Institution:
				consulta+= (" ?type SNAMetric:hasName ?nameType ." )


		if 'Betweenness_Centrality_less_than' in request.POST: #verifica se Degree_Centrality foi enviado na requisição
			Betweenness_Centrality_less_than = request.POST['Betweenness_Centrality_less_than']
			if Betweenness_Centrality_less_than:
				if  Betweenness_Centrality_less_than != "":
						texto = (""" FILTER( ?valueBC < """ + Betweenness_Centrality_less_than +") .")
						consulta+= ("?actor SNAMetric:hasSNAMetricBetweennessCentrality ?BetweennessCentrality . ?BetweennessCentrality SNAMetric:hasValue ?valueBC ." + texto)

		if 'Betweenness_Centrality_greater_than' in request.POST: #verifica se Degree_Centrality foi enviado na requisição
			Betweenness_Centrality_greater_than = request.POST['Betweenness_Centrality_greater_than']
			if Betweenness_Centrality_greater_than:
				if  Betweenness_Centrality_greater_than != "":
						texto = (""" FILTER( ?valueBC > """ + Betweenness_Centrality_greater_than +") .")
						consulta+= ("?actor SNAMetric:hasSNAMetricBetweennessCentrality ?BetweennessCentrality . ?BetweennessCentrality SNAMetric:hasValue ?valueBC ." + texto)

		if 'Closeness_Centrality_less_than' in request.POST: #verifica se Degree_Centrality foi enviado na requisição
			Closeness_Centrality_less_than = request.POST['Closeness_Centrality_less_than']
			if Closeness_Centrality_less_than:
				if  Closeness_Centrality_less_than != "":
						texto = (""" FILTER( ?valueCC < """ + Closeness_Centrality_less_than +") .")
						consulta+= ("?actor SNAMetric:hasSNAMetricClosenessCentrality ?ClosenessCentrality . ?ClosenessCentrality SNAMetric:hasValue ?valueCC ." + texto)

		if 'Closeness_Centrality_greater_than' in request.POST: #verifica se Degree_Centrality foi enviado na requisição
			Closeness_Centrality_greater_than = request.POST['Closeness_Centrality_greater_than']
			if Closeness_Centrality_greater_than:
				if  Closeness_Centrality_greater_than != "":
						texto = (""" FILTER( ?valueCC > """ + Closeness_Centrality_greater_than +") .")
						consulta+= ("?actor SNAMetric:hasSNAMetricClosenessCentrality ?ClosenessCentrality . ?ClosenessCentrality SNAMetric:hasValue ?valueCC ." + texto)

		if 'Degree_Centrality_less_than' in request.POST: #verifica se Degree_Centrality foi enviado na requisição
			Degree_Centrality_less_than = request.POST['Degree_Centrality_less_than']
			if Degree_Centrality_less_than:
				if  Degree_Centrality_less_than != "":
						texto = (""" FILTER( ?valueDC < """ + Degree_Centrality_less_than +") .")
						consulta+= ("?actor SNAMetric:hasSNAMetricDegreeCentrality ?DegreeCentrality . ?DegreeCentrality SNAMetric:hasValue ?valueDC ." + texto)


		if 'Degree_Centrality_greater_than' in request.POST: #verifica se Degree_Centrality foi enviado na requisição
			Degree_Centrality_greater_than = request.POST['Degree_Centrality_greater_than']
			if Degree_Centrality_greater_than:
				if  Degree_Centrality_greater_than != "":
						texto = (""" FILTER( ?valueDC > """ + Degree_Centrality_greater_than +") .")
						consulta+= ("?actor SNAMetric:hasSNAMetricDegreeCentrality ?DegreeCentrality . ?DegreeCentrality SNAMetric:hasValue ?valueDC ." + texto)

		if 'Average_Degree_less_than' in request.POST: #verifica se Degree_Centrality foi enviado na requisição
			Average_Degree_less_than = request.POST['Average_Degree_less_than']
			if Average_Degree_less_than:
				if  Average_Degree_less_than != "":
						texto = (""" FILTER( ?valorAverageDegree < """ + Average_Degree_less_than +") .")
						consulta+= ("?rede scnas:has_AverageDegree ?AverageDegree . ?AverageDegree SNAMetric:hasValue ?valorAverageDegree ." + texto)

		if 'Average_Degree_less_than' in request.POST: #verifica se Degree_Centrality foi enviado na requisição
			Average_Degree_less_than = request.POST['Average_Degree_less_than']
			if Average_Degree_less_than:
				if  Average_Degree_less_than != "":
						texto = (""" FILTER( ?valorAverageDegree < """ + Average_Degree_less_than +") .")
						consulta+= ("?rede scnas:has_AverageDegree ?AverageDegree . ?AverageDegree SNAMetric:hasValue ?valorAverageDegree ." + texto)


		if 'Average_Degree_greater_than' in request.POST: #verifica se Degree_Centrality foi enviado na requisição
			Average_Degree_greater_than = request.POST['Average_Degree_greater_than']
			if Average_Degree_greater_than:
				if  Average_Degree_greater_than != "":
						texto = (""" FILTER( ?valorAverageDegree > """ + Average_Degree_greater_than +") .")
						consulta+= (" ?rede scnas:has_AverageDegree ?AverageDegree . ?AverageDegree SNAMetric:hasValue ?valorAverageDegree . " + texto)

		if 'Component_less_than' in request.POST: #verifica se Degree_Centrality foi enviado na requisição
			Component_less_than = request.POST['Component_less_than']
			if Component_less_than:
				if  Component_less_than != "":
						texto = (""" FILTER( ?ValorComponent < """ + Component_less_than +") .")
						consulta+= (" ?rede SNAMetric:hasSNAMetricComponent ?Component . ?Component SNAMetric:hasValue ?ValorComponent . " + texto)

		if 'Component_greater_than' in request.POST: #verifica se Degree_Centrality foi enviado na requisição
			Component_greater_than = request.POST['Component_greater_than']
			if Component_greater_than:
				if  Component_greater_than != "":
						texto = (""" FILTER( ?ValorComponent > """ + Component_greater_than +") .")
						consulta+= (" ?rede SNAMetric:hasSNAMetricComponent ?Component . ?Component SNAMetric:hasValue ?ValorComponent . " + texto)

		if 'Density_less_than' in request.POST: #verifica se Degree_Centrality foi enviado na requisição
			Density_less_than = request.POST['Density_less_than']
			if Density_less_than:
				if  Density_less_than != "":
						texto = (""" FILTER( ?valorDensity < """ + Density_less_than +") .")
						consulta+= (" ?rede scnas:has_Density ?densidade . ?densidade SNAMetric:hasValue ?valorDensity . " + texto)

		if 'Density_greater_than' in request.POST: #verifica se Degree_Centrality foi enviado na requisição
			Density_greater_than = request.POST['Density_greater_than']
			if Density_greater_than:
				if  Density_greater_than != "":
						texto = (""" FILTER( ?valorDensity > """ + Density_greater_than +") .")
						consulta+= (" ?rede scnas:has_Density ?densidade . ?densidade SNAMetric:hasValue ?valorDensity . " + texto)

		if 'Institution_Name' in request.POST: #verifica se Degree_Centrality foi enviado na requisição
			Institution_Name = request.POST['Institution_Name']
			if Institution_Name:
				if  Institution_Name != "":
						texto = (""" ?type SNAMetric:hasName '""" + Institution_Name +"' .")
						consulta+= ("  ?assertion scnas:has_Type ?type . " + texto)			

		if 'Knowledge_Area_Name' in request.POST: #verifica se Degree_Centrality foi enviado na requisição
			Knowledge_Area_Name = request.POST['Knowledge_Area_Name']
			if Knowledge_Area_Name:
				if  Knowledge_Area_Name != "":
					texto = (""" ?KnowledgeArea SNAMetric:hasName '""" + Knowledge_Area_Name +"' .")							
					consulta += ("?type scnas:has_KnowledgeArea ?KnowledgeArea ." + texto	)	


		if 'Degree_Centrality' in request.POST or 'Closeness_Centrality' in request.POST or 'Betweenness_Centrality' in request.POST:
			consulta+=(" ?assertion scnas:has_Network ?rede .")
			Actor= "Actor"
			consulta += ("""
					?rede scnas:has_Actor ?actor.
 					?actor SNAMetric:hasName ?nameActor .""")
			if 'Degree_Centrality' in request.POST: #verifica se Degree_Centrality foi enviado na requisição
	 			Degree_Centrality = request.POST['Degree_Centrality']
	 			if Degree_Centrality:
	 				Degree = "Degree Centrality " 							
	 				consulta += ("""
					?actor SNAMetric:hasSNAMetricDegreeCentrality ?DegreeCentrality .
					?DegreeCentrality SNAMetric:hasValue ?valueDC .""")
			if 'Closeness_Centrality' in request.POST: #verifica se Closeness_Centrality foi enviado na requisição
				Closeness_Centrality = request.POST['Closeness_Centrality']
				if Closeness_Centrality:
					Closeness = "Closeness Centrality "							
					consulta += ("""
					?actor SNAMetric:hasSNAMetricClosenessCentrality ?ClosenessCentrality .
					?ClosenessCentrality SNAMetric:hasValue ?valueCC .""")
			if 'Betweenness_Centrality' in request.POST: #verifica se Betweenness_Centrality foi enviado na requisição
				Betweenness_Centrality = request.POST['Betweenness_Centrality']
				if Betweenness_Centrality:
					Betweenness = "Betweenness Centrality "						
					consulta += ("""
					?actor SNAMetric:hasSNAMetricBetweennessCentrality ?BetweennessCentrality .
					?BetweennessCentrality SNAMetric:hasValue ?valueBC .""")

		if 'Density' in request.POST or 'Component' in request.POST or 	'Average_Degree' in request.POST or 'Actors_Number' in request.POST or 'Edges_Number' in request.POST:
			consulta+=(" ?assertion scnas:has_Network ?rede .")		
			if 'Density' in request.POST: #verifica se Degree_Centrality foi enviado na requisição
	 			Density = request.POST['Density']
	 			if Density:
	 				Density_ = "Density"
	 				consulta += ("""
					?rede scnas:has_Density ?densidade .
		 			?densidade SNAMetric:hasValue ?valorDensity .""") 
			if 'Component' in request.POST: #verifica se Degree_Centrality foi enviado na requisição
	 			Component = request.POST['Component']
	 			if Component:
	 				consulta += ("""
					?rede SNAMetric:hasSNAMetricComponent ?Component .
	 				?Component SNAMetric:hasValue ?ValorComponent. """) 
			if 'Average_Degree' in request.POST: #verifica se Degree_Centrality foi enviado na requisição
	 			Average_Degree = request.POST['Average_Degree']
	 			if Average_Degree:
	 				consulta += ("""
					?rede scnas:has_AverageDegree ?AverageDegree .
					 ?AverageDegree SNAMetric:hasValue ?valorAverageDegree .""") 
			if 'Actors_Number' in request.POST: #verifica se Degree_Centrality foi enviado na requisição
	 			Actors_Number = request.POST['Actors_Number']
	 			if Actors_Number:
	 				consulta += ("""
					?rede scnas:has_ActorsNumber ?ActorsNumber .
	 				?ActorsNumber SNAMetric:hasValue ?ValueActorsNumber .""")
			if 'Edges_Number' in request.POST: #verifica se Degree_Centrality foi enviado na requisição
	 			Edges_Number = request.POST['Edges_Number']
	 			if Edges_Number:
	 				consulta += ("""
					?rede scnas:has_EdgesNumber ?EdgesNumber .
					?EdgesNumber SNAMetric:hasValue ?ValueEdgesNumber .""")


		consulta += ("""
		}
		LIMIT 10000""")

		sparql.setQuery(consulta)
		sparql.setReturnFormat(JSON)
		results = sparql.query().convert()

		def remove_repetidos(lista):
		    l = []
		    for i in lista:
		        if i not in l:
		            l.append(i)
		    l.sort()
		    return l

		


		for result in results["results"]["bindings"]:
			for var in results["head"]["vars"]:
				if var == "anoinicio":
					Inicio = "Inicio"
					listaAnoInicio.append(result[var]['value'])
				if var == "anofim":
					Fim = "Fim"
					listaAnoFim.append(result[var]['value'])	
				if var == "URL":
					DOI= "DOI"
					listaURL.append(result[var]['value'])
				if var == "nameLocation":
					Location = "Location"
					ListaLocation.append(result[var]['value'])
				if var == "nameType":
					Institution= "Institution"
					listaInstitution.append(result[var]['value'])
				if var == "title":
					Titles = "SCNAS"
					listaTitulos.append(result[var]['value'])
					aux= remove_repetidos(listaTitulos)
					counttitles= len(aux)	

				if 'Degree_Centrality' in request.POST or 'Closeness_Centrality' in request.POST or 'Betweenness_Centrality' in request.POST:
										
					if var == "nameActor":
						listaActor.append(result[var]['value'])
					if 'Degree_Centrality' in request.POST: #verifica se Degree_Centrality foi enviado na requisição
			 			Degree_Centrality = request.POST['Degree_Centrality']
			 			if Degree_Centrality:
			 				if var == "valueDC":
			 					listaDC.append(result[var]['value'])
					if 'Closeness_Centrality' in request.POST: #verifica se Closeness_Centrality foi enviado na requisição
						Closeness_Centrality = request.POST['Closeness_Centrality']
						if Closeness_Centrality:
							if var == "valueCC":
								listaCC.append(result[var]['value'])
					if 'Betweenness_Centrality' in request.POST: #verifica se Betweenness_Centrality foi enviado na requisição
						Betweenness_Centrality = request.POST['Betweenness_Centrality']
						if Betweenness_Centrality:
							if var == "valueBC":
								listaBC.append(result[var]['value'])
				if 'Density' in request.POST or 'Component' in request.POST or 'Average_Degree' in request.POST or 'Actors_Number' in request.POST or 'Edges_Number' in request.POST:
					if 'Density' in request.POST: #verifica se Betweenness_Centrality foi enviado na requisição
						Densidade= "Density"
						Density = request.POST['Density']
						if Density:
							if var == "valorDensity":
								listaDensity.append(result[var]['value'])
					if 'Component' in request.POST: #verifica se Betweenness_Centrality foi enviado na requisição
						Compo="Component"
						Component = request.POST['Component']
						if Component:
							if var == "ValorComponent":
								listaComponentes.append(result[var]['value'])
					if 'Average_Degree' in request.POST: #verifica se Betweenness_Centrality foi enviado na requisição
						Average_Degree = request.POST['Average_Degree']
						if Average_Degree:
							Average= "Average Degree"
							if var == "valorAverageDegree":
								listaAverageDegree.append(result[var]['value'])
					if 'Actors_Number' in request.POST: #verifica se Betweenness_Centrality foi enviado na requisição
						Actors_Number = request.POST['Actors_Number']
						if Actors_Number:
							AN= "Actors Number"
							if var == "ValueActorsNumber":
								listaActorsNumber.append(result[var]['value'])

					if 'Edges_Number' in request.POST: #verifica se Betweenness_Centrality foi enviado na requisição
						Edges_Number = request.POST['Edges_Number']
						if Edges_Number:
							EN= "Edges Number"
							if var == "ValueEdgesNumber":
								listaEdgesNumber.append(result[var]['value'])




	return render(request, "HEI.html", {'InstitutionOther':InstitutionOther, 'filtroInstitution':filtroInstitution, 'ActorMetrics': ActorMetrics, 'NetworkMetrics': NetworkMetrics, 'filtroKnowledgeArea':filtroKnowledgeArea, 'filtroNetworkMetrics': filtroNetworkMetrics, 'filtroActorsMetrics': filtroActorsMetrics, 'filtroPeriodic':filtroPeriodic, 'Atores': listaActor, 'DCs':listaDC, 'CCs':listaCC, 'BCs': listaBC, 'URLs': listaURL, 'Titulos': listaTitle, 'Densities': listaDensity, 'Componentes': listaComponentes, 'AverageDegrees': listaAverageDegree, "Regions": listaRegion, 
'Location': Location, 'Betweenness': Betweenness, 'Closeness': Closeness, 'Degree': Degree, 'DOI': DOI, 'Locations': ListaLocation, 'Actor': Actor, 'Densidade':Densidade, 'titulo': titulo, 'Compo':Compo, 'Averag': Average, 'numerodeatores': listaActorsNumber, 'AN':AN, 'EN':EN, "numerodeedges": listaEdgesNumber, "Institution": Institution, "listaInstitution":listaInstitution, 'listaTitles': listaTitulos, "Titles":Titles, 'counttitles':counttitles, 'listaAnoFim':listaAnoFim, 'listaAnoInicio':listaAnoInicio,'Inicio':Inicio, 'Fim': Fim })

def Research(request):

	sparql = SPARQLWrapper("http://localhost:3030/SCNAS")
	consulta = ("""
prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#>
prefix owl: <http://www.w3.org/2002/07/owl#>
PREFIX xmlns:<http://www.nanopub.org/nschema>
PREFIX base:<http://www.nanopub.org/nschema>
PREFIX dc:<http://purl.org/dc/elements/1.1/>
PREFIX np:<http://www.nanopub.org/nschema#>
PREFIX ns:<http://www.w3.org/2003/06/sw-vocab-status/ns#>
PREFIX owl:<http://www.w3.org/2002/07/owl#>
PREFIX xml:<http://www.w3.org/XML/1998/namespace>
PREFIX foaf:<http://xmlns.com/foaf/0.1/>
PREFIX prov:<http://www.w3.org/ns/prov#>
PREFIX rdfg:<http://www.w3.org/2004/03/trix/rdfg-1/>
PREFIX skos:<http://www.w3.org/2004/02/skos/core#>
PREFIX time:<http://www.w3.org/2006/time#>
PREFIX fabio:<http://purl.org/spar/fabio/>
PREFIX terms:<http://purl.org/dc/terms/>
PREFIX datacite:<http://purl.org/spar/datacite/>
PREFIX SNAMetric:<http://ns.inria.fr/semsna/2009/06/21/SNAMetric#>
PREFIX XMLSchema:<http://www.w3.org/2000/10/XMLSchema#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX scnas:<http://www.semanticweb.org/cliente/ontologies/2019/9/SCNAS#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX sc: <http://purl.org/science/owl/sciencecommons/>

SELECT  *
WHERE{
 ?nanopublication np:hasAssertion ?assertion .
 ?nanopublication np:hasProvenance ?provenance .
 ?provenance datacite:usesIdentifierScheme ?DOI .
 ?DOI fabio:hasURL ?URL .
 ?provenance dc:title ?title .
 ?assertion rdf:type np:Assertion .
 ?assertion scnas:has_Type ?type .
 ?type rdf:type scnas:Research_Institution .

""")

	listaActor=[]
	listaDC= []
	listaCC= []
	listaBC= []
	listaURL= []
	listaTitulos= []


	listaTitle= []
	listaDensity= []
	listaComponentes= []
	listaAverageDegree = []
	ListaLocation= []
	listaActorsNumber = []
	listaEdgesNumber= []
	listaInstitution=[]
	listaRegion=[]
	aux=[]

	Institution="No"
	Location = "No"
	Betweenness = "No"
	Closeness = "No"
	Degree = "No"
	DOI = "No"
	#MÉTRICAS DE ATORES
	Actor="No"
	Densidade= "No"
	titulo = "No"
	Compo="No"
	Average= "No"
	AN= "No"
	EN= "No"
	Titles="No"
	counttitles=0
	Fim= "No"
	Inicio="No"
	listaAnoInicio=[]
	listaAnoFim=[]


	if request.method == "POST":

		if 'Network_Time' in request.POST: #verifica se Degree_Centrality foi enviado na requisição
			Network_Time = request.POST['Network_Time']
			if Network_Time:
				consulta+= ("""  ?assertion scnas:has_Network ?rede . 
				?rede scnas:has_Time ?tempo.
 				?tempo time:hasBeginning ?inicio .
 				?tempo time:hasEnd ?fim .
 				?inicio time:year ?anoinicio.
 				?fim time:year ?anofim .""" )


		if 'Region' in request.POST: #verifica se Degree_Centrality foi enviado na requisição
			Region = request.POST['Region']
			if Region:
				consulta+= ("?type scnas:has_Location ?Location .  ?Location SNAMetric:hasName ?nameLocation ." )


		if 'High_Education_Institution' in request.POST: #verifica se Degree_Centrality foi enviado na requisição
			High_Education_Institution = request.POST['High_Education_Institution']
			if High_Education_Institution:
				consulta+= (" ?type SNAMetric:hasName ?nameType ." )


		if 'Betweenness_Centrality_less_than' in request.POST: #verifica se Degree_Centrality foi enviado na requisição
			Betweenness_Centrality_less_than = request.POST['Betweenness_Centrality_less_than']
			if Betweenness_Centrality_less_than:
				if  Betweenness_Centrality_less_than != "":
						texto = (""" FILTER( ?valueBC < """ + Betweenness_Centrality_less_than +") .")
						consulta+= ("?actor SNAMetric:hasSNAMetricBetweennessCentrality ?BetweennessCentrality . ?BetweennessCentrality SNAMetric:hasValue ?valueBC ." + texto)

		if 'Betweenness_Centrality_greater_than' in request.POST: #verifica se Degree_Centrality foi enviado na requisição
			Betweenness_Centrality_greater_than = request.POST['Betweenness_Centrality_greater_than']
			if Betweenness_Centrality_greater_than:
				if  Betweenness_Centrality_greater_than != "":
						texto = (""" FILTER( ?valueBC > """ + Betweenness_Centrality_greater_than +") .")
						consulta+= ("?actor SNAMetric:hasSNAMetricBetweennessCentrality ?BetweennessCentrality . ?BetweennessCentrality SNAMetric:hasValue ?valueBC ." + texto)

		if 'Closeness_Centrality_less_than' in request.POST: #verifica se Degree_Centrality foi enviado na requisição
			Closeness_Centrality_less_than = request.POST['Closeness_Centrality_less_than']
			if Closeness_Centrality_less_than:
				if  Closeness_Centrality_less_than != "":
						texto = (""" FILTER( ?valueCC < """ + Closeness_Centrality_less_than +") .")
						consulta+= ("?actor SNAMetric:hasSNAMetricClosenessCentrality ?ClosenessCentrality . ?ClosenessCentrality SNAMetric:hasValue ?valueCC ." + texto)

		if 'Closeness_Centrality_greater_than' in request.POST: #verifica se Degree_Centrality foi enviado na requisição
			Closeness_Centrality_greater_than = request.POST['Closeness_Centrality_greater_than']
			if Closeness_Centrality_greater_than:
				if  Closeness_Centrality_greater_than != "":
						texto = (""" FILTER( ?valueCC > """ + Closeness_Centrality_greater_than +") .")
						consulta+= ("?actor SNAMetric:hasSNAMetricClosenessCentrality ?ClosenessCentrality . ?ClosenessCentrality SNAMetric:hasValue ?valueCC ." + texto)

		if 'Degree_Centrality_less_than' in request.POST: #verifica se Degree_Centrality foi enviado na requisição
			Degree_Centrality_less_than = request.POST['Degree_Centrality_less_than']
			if Degree_Centrality_less_than:
				if  Degree_Centrality_less_than != "":
						texto = (""" FILTER( ?valueDC < """ + Degree_Centrality_less_than +") .")
						consulta+= ("?actor SNAMetric:hasSNAMetricDegreeCentrality ?DegreeCentrality . ?DegreeCentrality SNAMetric:hasValue ?valueDC ." + texto)


		if 'Degree_Centrality_greater_than' in request.POST: #verifica se Degree_Centrality foi enviado na requisição
			Degree_Centrality_greater_than = request.POST['Degree_Centrality_greater_than']
			if Degree_Centrality_greater_than:
				if  Degree_Centrality_greater_than != "":
						texto = (""" FILTER( ?valueDC > """ + Degree_Centrality_greater_than +") .")
						consulta+= ("?actor SNAMetric:hasSNAMetricDegreeCentrality ?DegreeCentrality . ?DegreeCentrality SNAMetric:hasValue ?valueDC ." + texto)

		if 'Average_Degree_less_than' in request.POST: #verifica se Degree_Centrality foi enviado na requisição
			Average_Degree_less_than = request.POST['Average_Degree_less_than']
			if Average_Degree_less_than:
				if  Average_Degree_less_than != "":
						texto = (""" FILTER( ?valorAverageDegree < """ + Average_Degree_less_than +") .")
						consulta+= ("?rede scnas:has_AverageDegree ?AverageDegree . ?AverageDegree SNAMetric:hasValue ?valorAverageDegree ." + texto)

		if 'Average_Degree_less_than' in request.POST: #verifica se Degree_Centrality foi enviado na requisição
			Average_Degree_less_than = request.POST['Average_Degree_less_than']
			if Average_Degree_less_than:
				if  Average_Degree_less_than != "":
						texto = (""" FILTER( ?valorAverageDegree < """ + Average_Degree_less_than +") .")
						consulta+= ("?rede scnas:has_AverageDegree ?AverageDegree . ?AverageDegree SNAMetric:hasValue ?valorAverageDegree ." + texto)


		if 'Average_Degree_greater_than' in request.POST: #verifica se Degree_Centrality foi enviado na requisição
			Average_Degree_greater_than = request.POST['Average_Degree_greater_than']
			if Average_Degree_greater_than:
				if  Average_Degree_greater_than != "":
						texto = (""" FILTER( ?valorAverageDegree > """ + Average_Degree_greater_than +") .")
						consulta+= (" ?rede scnas:has_AverageDegree ?AverageDegree . ?AverageDegree SNAMetric:hasValue ?valorAverageDegree . " + texto)

		if 'Component_less_than' in request.POST: #verifica se Degree_Centrality foi enviado na requisição
			Component_less_than = request.POST['Component_less_than']
			if Component_less_than:
				if  Component_less_than != "":
						texto = (""" FILTER( ?ValorComponent < """ + Component_less_than +") .")
						consulta+= (" ?rede SNAMetric:hasSNAMetricComponent ?Component . ?Component SNAMetric:hasValue ?ValorComponent . " + texto)

		if 'Component_greater_than' in request.POST: #verifica se Degree_Centrality foi enviado na requisição
			Component_greater_than = request.POST['Component_greater_than']
			if Component_greater_than:
				if  Component_greater_than != "":
						texto = (""" FILTER( ?ValorComponent > """ + Component_greater_than +") .")
						consulta+= (" ?rede SNAMetric:hasSNAMetricComponent ?Component . ?Component SNAMetric:hasValue ?ValorComponent . " + texto)

		if 'Density_less_than' in request.POST: #verifica se Degree_Centrality foi enviado na requisição
			Density_less_than = request.POST['Density_less_than']
			if Density_less_than:
				if  Density_less_than != "":
						texto = (""" FILTER( ?valorDensity < """ + Density_less_than +") .")
						consulta+= (" ?rede scnas:has_Density ?densidade . ?densidade SNAMetric:hasValue ?valorDensity . " + texto)

		if 'Density_greater_than' in request.POST: #verifica se Degree_Centrality foi enviado na requisição
			Density_greater_than = request.POST['Density_greater_than']
			if Density_greater_than:
				if  Density_greater_than != "":
						texto = (""" FILTER( ?valorDensity > """ + Density_greater_than +") .")
						consulta+= (" ?rede scnas:has_Density ?densidade . ?densidade SNAMetric:hasValue ?valorDensity . " + texto)

		if 'Institution_Name' in request.POST: #verifica se Degree_Centrality foi enviado na requisição
			Institution_Name = request.POST['Institution_Name']
			if Institution_Name:
				if  Institution_Name != "":
						texto = (""" ?type SNAMetric:hasName '""" + Institution_Name +"' .")
						consulta+= ("  ?assertion scnas:has_Type ?type . " + texto)			

		if 'Knowledge_Area_Name' in request.POST: #verifica se Degree_Centrality foi enviado na requisição
			Knowledge_Area_Name = request.POST['Knowledge_Area_Name']
			if Knowledge_Area_Name:
				if  Knowledge_Area_Name != "":
					texto = (""" ?KnowledgeArea SNAMetric:hasName '""" + Knowledge_Area_Name +"' .")							
					consulta += ("?type scnas:has_KnowledgeArea ?KnowledgeArea ." + texto	)	


		if 'Degree_Centrality' in request.POST or 'Closeness_Centrality' in request.POST or 'Betweenness_Centrality' in request.POST:
			consulta+=(" ?assertion scnas:has_Network ?rede .")
			Actor= "Actor"
			consulta += ("""
					?rede scnas:has_Actor ?actor.
 					?actor SNAMetric:hasName ?nameActor .""")
			if 'Degree_Centrality' in request.POST: #verifica se Degree_Centrality foi enviado na requisição
	 			Degree_Centrality = request.POST['Degree_Centrality']
	 			if Degree_Centrality:
	 				Degree = "Degree Centrality " 							
	 				consulta += ("""
					?actor SNAMetric:hasSNAMetricDegreeCentrality ?DegreeCentrality .
					?DegreeCentrality SNAMetric:hasValue ?valueDC .""")
			if 'Closeness_Centrality' in request.POST: #verifica se Closeness_Centrality foi enviado na requisição
				Closeness_Centrality = request.POST['Closeness_Centrality']
				if Closeness_Centrality:
					Closeness = "Closeness Centrality "							
					consulta += ("""
					?actor SNAMetric:hasSNAMetricClosenessCentrality ?ClosenessCentrality .
					?ClosenessCentrality SNAMetric:hasValue ?valueCC .""")
			if 'Betweenness_Centrality' in request.POST: #verifica se Betweenness_Centrality foi enviado na requisição
				Betweenness_Centrality = request.POST['Betweenness_Centrality']
				if Betweenness_Centrality:
					Betweenness = "Betweenness Centrality "						
					consulta += ("""
					?actor SNAMetric:hasSNAMetricBetweennessCentrality ?BetweennessCentrality .
					?BetweennessCentrality SNAMetric:hasValue ?valueBC .""")

		if 'Density' in request.POST or 'Component' in request.POST or 	'Average_Degree' in request.POST or 'Actors_Number' in request.POST or 'Edges_Number' in request.POST:
			consulta+=(" ?assertion scnas:has_Network ?rede .")		
			if 'Density' in request.POST: #verifica se Degree_Centrality foi enviado na requisição
	 			Density = request.POST['Density']
	 			if Density:
	 				Density_ = "Density"
	 				consulta += ("""
					?rede scnas:has_Density ?densidade .
		 			?densidade SNAMetric:hasValue ?valorDensity .""") 
			if 'Component' in request.POST: #verifica se Degree_Centrality foi enviado na requisição
	 			Component = request.POST['Component']
	 			if Component:
	 				consulta += ("""
					?rede SNAMetric:hasSNAMetricComponent ?Component .
	 				?Component SNAMetric:hasValue ?ValorComponent. """) 
			if 'Average_Degree' in request.POST: #verifica se Degree_Centrality foi enviado na requisição
	 			Average_Degree = request.POST['Average_Degree']
	 			if Average_Degree:
	 				consulta += ("""
					?rede scnas:has_AverageDegree ?AverageDegree .
					 ?AverageDegree SNAMetric:hasValue ?valorAverageDegree .""") 
			if 'Actors_Number' in request.POST: #verifica se Degree_Centrality foi enviado na requisição
	 			Actors_Number = request.POST['Actors_Number']
	 			if Actors_Number:
	 				consulta += ("""
					?rede scnas:has_ActorsNumber ?ActorsNumber .
	 				?ActorsNumber SNAMetric:hasValue ?ValueActorsNumber .""")
			if 'Edges_Number' in request.POST: #verifica se Degree_Centrality foi enviado na requisição
	 			Edges_Number = request.POST['Edges_Number']
	 			if Edges_Number:
	 				consulta += ("""
					?rede scnas:has_EdgesNumber ?EdgesNumber .
					?EdgesNumber SNAMetric:hasValue ?ValueEdgesNumber .""")


		consulta += ("""
		}
		LIMIT 10000""")

		sparql.setQuery(consulta)
		sparql.setReturnFormat(JSON)
		results = sparql.query().convert()

		def remove_repetidos(lista):
		    l = []
		    for i in lista:
		        if i not in l:
		            l.append(i)
		    l.sort()
		    return l

		


		for result in results["results"]["bindings"]:
			for var in results["head"]["vars"]:
				if var == "anoinicio":
					Inicio = "Inicio"
					listaAnoInicio.append(result[var]['value'])
				if var == "anofim":
					Fim = "Fim"
					listaAnoFim.append(result[var]['value'])	
				if var == "URL":
					DOI= "DOI"
					listaURL.append(result[var]['value'])
				if var == "nameLocation":
					Location = "Location"
					ListaLocation.append(result[var]['value'])
				if var == "nameType":
					Institution= "Institution"
					listaInstitution.append(result[var]['value'])
				if var == "title":
					Titles = "SCNAS"
					listaTitulos.append(result[var]['value'])
					aux= remove_repetidos(listaTitulos)
					counttitles= len(aux)	

				if 'Degree_Centrality' in request.POST or 'Closeness_Centrality' in request.POST or 'Betweenness_Centrality' in request.POST:
										
					if var == "nameActor":
						listaActor.append(result[var]['value'])
					if 'Degree_Centrality' in request.POST: #verifica se Degree_Centrality foi enviado na requisição
			 			Degree_Centrality = request.POST['Degree_Centrality']
			 			if Degree_Centrality:
			 				if var == "valueDC":
			 					listaDC.append(result[var]['value'])
					if 'Closeness_Centrality' in request.POST: #verifica se Closeness_Centrality foi enviado na requisição
						Closeness_Centrality = request.POST['Closeness_Centrality']
						if Closeness_Centrality:
							if var == "valueCC":
								listaCC.append(result[var]['value'])
					if 'Betweenness_Centrality' in request.POST: #verifica se Betweenness_Centrality foi enviado na requisição
						Betweenness_Centrality = request.POST['Betweenness_Centrality']
						if Betweenness_Centrality:
							if var == "valueBC":
								listaBC.append(result[var]['value'])
				if 'Density' in request.POST or 'Component' in request.POST or 'Average_Degree' in request.POST or 'Actors_Number' in request.POST or 'Edges_Number' in request.POST:
					if 'Density' in request.POST: #verifica se Betweenness_Centrality foi enviado na requisição
						Densidade= "Density"
						Density = request.POST['Density']
						if Density:
							if var == "valorDensity":
								listaDensity.append(result[var]['value'])
					if 'Component' in request.POST: #verifica se Betweenness_Centrality foi enviado na requisição
						Compo="Component"
						Component = request.POST['Component']
						if Component:
							if var == "ValorComponent":
								listaComponentes.append(result[var]['value'])
					if 'Average_Degree' in request.POST: #verifica se Betweenness_Centrality foi enviado na requisição
						Average_Degree = request.POST['Average_Degree']
						if Average_Degree:
							Average= "Average Degree"
							if var == "valorAverageDegree":
								listaAverageDegree.append(result[var]['value'])
					if 'Actors_Number' in request.POST: #verifica se Betweenness_Centrality foi enviado na requisição
						Actors_Number = request.POST['Actors_Number']
						if Actors_Number:
							AN= "Actors Number"
							if var == "ValueActorsNumber":
								listaActorsNumber.append(result[var]['value'])

					if 'Edges_Number' in request.POST: #verifica se Betweenness_Centrality foi enviado na requisição
						Edges_Number = request.POST['Edges_Number']
						if Edges_Number:
							EN= "Edges Number"
							if var == "ValueEdgesNumber":
								listaEdgesNumber.append(result[var]['value'])




	return render(request, "researchInstitution.html", {'InstitutionOther':InstitutionOther, 'filtroInstitution':filtroInstitution, 'ActorMetrics': ActorMetrics, 'NetworkMetrics': NetworkMetrics, 'filtroKnowledgeArea':filtroKnowledgeArea, 'filtroNetworkMetrics': filtroNetworkMetrics, 'filtroActorsMetrics': filtroActorsMetrics, 'filtroPeriodic':filtroPeriodic, 'Atores': listaActor, 'DCs':listaDC, 'CCs':listaCC, 'BCs': listaBC, 'URLs': listaURL, 'Titulos': listaTitle, 'Densities': listaDensity, 'Componentes': listaComponentes, 'AverageDegrees': listaAverageDegree, "Regions": listaRegion, 
'Location': Location, 'Betweenness': Betweenness, 'Closeness': Closeness, 'Degree': Degree, 'DOI': DOI, 'Locations': ListaLocation, 'Actor': Actor, 'Densidade':Densidade, 'titulo': titulo, 'Compo':Compo, 'Averag': Average, 'numerodeatores': listaActorsNumber, 'AN':AN, 'EN':EN, "numerodeedges": listaEdgesNumber, "Institution": Institution, "listaInstitution":listaInstitution, 'listaTitles': listaTitulos, "Titles":Titles, 'counttitles':counttitles, 'listaAnoFim':listaAnoFim, 'listaAnoInicio':listaAnoInicio,'Inicio':Inicio, 'Fim': Fim})


def Geographic(request):
	sparql = SPARQLWrapper("http://localhost:3030/SCNAS")
	consulta = ("""
prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#>
prefix owl: <http://www.w3.org/2002/07/owl#>
PREFIX xmlns:<http://www.nanopub.org/nschema>
PREFIX base:<http://www.nanopub.org/nschema>
PREFIX dc:<http://purl.org/dc/elements/1.1/>
PREFIX np:<http://www.nanopub.org/nschema#>
PREFIX ns:<http://www.w3.org/2003/06/sw-vocab-status/ns#>
PREFIX owl:<http://www.w3.org/2002/07/owl#>
PREFIX xml:<http://www.w3.org/XML/1998/namespace>
PREFIX foaf:<http://xmlns.com/foaf/0.1/>
PREFIX prov:<http://www.w3.org/ns/prov#>
PREFIX rdfg:<http://www.w3.org/2004/03/trix/rdfg-1/>
PREFIX skos:<http://www.w3.org/2004/02/skos/core#>
PREFIX time:<http://www.w3.org/2006/time#>
PREFIX fabio:<http://purl.org/spar/fabio/>
PREFIX terms:<http://purl.org/dc/terms/>
PREFIX datacite:<http://purl.org/spar/datacite/>
PREFIX SNAMetric:<http://ns.inria.fr/semsna/2009/06/21/SNAMetric#>
PREFIX XMLSchema:<http://www.w3.org/2000/10/XMLSchema#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX scnas:<http://www.semanticweb.org/cliente/ontologies/2019/9/SCNAS#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX sc: <http://purl.org/science/owl/sciencecommons/>

SELECT  *
WHERE{
 ?nanopublication np:hasAssertion ?assertion .
 ?nanopublication np:hasProvenance ?provenance .
 ?provenance datacite:usesIdentifierScheme ?DOI .
 ?DOI fabio:hasURL ?URL . 
 ?provenance dc:title ?title .
 ?assertion rdf:type np:Assertion .
 ?assertion scnas:has_Type ?type .
 ?type rdf:type scnas:Geographic.





""")


#	sparql.setQuery(consulta)
	
	
	#DC = []
	#CC= []
	#BC= []



	listaActor=[]
	listaDC= []
	listaCC= []
	listaBC= []
	listaURL= []
	listaTitulos= []
	listaRegion= []


	listaTitle= []
	listaDensity= []
	listaComponentes= []
	listaAverageDegree = []
	ListaLocation= []
	listaActorsNumber = []
	listaEdgesNumber= []
	listaAC=[]
	aux=[]



	Location = "No"
	Betweenness = "No"
	Closeness = "No"
	Degree = "No"
	DOI = "No"
	#MÉTRICAS DE ATORES
	Actor="No"
	Densidade= "No"
	titulo = "No"
	Compo="No"
	Average= "No"
	AN= "No"
	EN= "No"
	AC="No"
	Titles="No"
	counttitles = 0

	Fim= "No"
	Inicio="No"
	listaAnoInicio=[]
	listaAnoFim=[]


	if request.method == "POST":
		if 'Network_Time' in request.POST: #verifica se Degree_Centrality foi enviado na requisição
			Network_Time = request.POST['Network_Time']
			if Network_Time:
				consulta+= ("""  ?assertion scnas:has_Network ?rede . 
				?rede scnas:has_Time ?tempo.
 				?tempo time:hasBeginning ?inicio .
 				?tempo time:hasEnd ?fim .
 				?inicio time:year ?anoinicio.
 				?fim time:year ?anofim .""" )


		if 'Region_Name' in request.POST: #verifica se Degree_Centrality foi enviado na requisição
			Region_Name = request.POST['Region_Name']
			if Region_Name:
				if  Region_Name != "":
						texto = ("""  ?location SNAMetric:hasName '""" + Region_Name +"' .")
						consulta+= (" ?type scnas:has_Location ?location." + texto)	
		if 'Knowledge_Area' in request.POST: #verifica se Degree_Centrality foi enviado na requisição
			Knowledge_Area = request.POST['Knowledge_Area']
			if Knowledge_Area:
				consulta+= ("  ?type rdf:type scnas:Knowledge_Area.  ?type SNAMetric:hasName ?nameType ." )

		if 'Betweenness_Centrality_less_than' in request.POST: #verifica se Degree_Centrality foi enviado na requisição
			Betweenness_Centrality_less_than = request.POST['Betweenness_Centrality_less_than']
			if Betweenness_Centrality_less_than:
				if  Betweenness_Centrality_less_than != "":
						texto = (""" FILTER( ?valueBC < """ + Betweenness_Centrality_less_than +") .")
						consulta+= ("?actor SNAMetric:hasSNAMetricBetweennessCentrality ?BetweennessCentrality . ?BetweennessCentrality SNAMetric:hasValue ?valueBC ." + texto)

		if 'Betweenness_Centrality_greater_than' in request.POST: #verifica se Degree_Centrality foi enviado na requisição
			Betweenness_Centrality_greater_than = request.POST['Betweenness_Centrality_greater_than']
			if Betweenness_Centrality_greater_than:
				if  Betweenness_Centrality_greater_than != "":
						texto = (""" FILTER( ?valueBC > """ + Betweenness_Centrality_greater_than +") .")
						consulta+= ("?actor SNAMetric:hasSNAMetricBetweennessCentrality ?BetweennessCentrality . ?BetweennessCentrality SNAMetric:hasValue ?valueBC ." + texto)

		if 'Closeness_Centrality_less_than' in request.POST: #verifica se Degree_Centrality foi enviado na requisição
			Closeness_Centrality_less_than = request.POST['Closeness_Centrality_less_than']
			if Closeness_Centrality_less_than:
				if  Closeness_Centrality_less_than != "":
						texto = (""" FILTER( ?valueCC < """ + Closeness_Centrality_less_than +") .")
						consulta+= ("?actor SNAMetric:hasSNAMetricClosenessCentrality ?ClosenessCentrality . ?ClosenessCentrality SNAMetric:hasValue ?valueCC ." + texto)

		if 'Closeness_Centrality_greater_than' in request.POST: #verifica se Degree_Centrality foi enviado na requisição
			Closeness_Centrality_greater_than = request.POST['Closeness_Centrality_greater_than']
			if Closeness_Centrality_greater_than:
				if  Closeness_Centrality_greater_than != "":
						texto = (""" FILTER( ?valueCC > """ + Closeness_Centrality_greater_than +") .")
						consulta+= ("?actor SNAMetric:hasSNAMetricClosenessCentrality ?ClosenessCentrality . ?ClosenessCentrality SNAMetric:hasValue ?valueCC ." + texto)

		if 'Degree_Centrality_less_than' in request.POST: #verifica se Degree_Centrality foi enviado na requisição
			Degree_Centrality_less_than = request.POST['Degree_Centrality_less_than']
			if Degree_Centrality_less_than:
				if  Degree_Centrality_less_than != "":
						texto = (""" FILTER( ?valueDC < """ + Degree_Centrality_less_than +") .")
						consulta+= ("?actor SNAMetric:hasSNAMetricDegreeCentrality ?DegreeCentrality . ?DegreeCentrality SNAMetric:hasValue ?valueDC ." + texto)


		if 'Degree_Centrality_greater_than' in request.POST: #verifica se Degree_Centrality foi enviado na requisição
			Degree_Centrality_greater_than = request.POST['Degree_Centrality_greater_than']
			if Degree_Centrality_greater_than:
				if  Degree_Centrality_greater_than != "":
						texto = (""" FILTER( ?valueDC > """ + Degree_Centrality_greater_than +") .")
						consulta+= ("?actor SNAMetric:hasSNAMetricDegreeCentrality ?DegreeCentrality . ?DegreeCentrality SNAMetric:hasValue ?valueDC ." + texto)

		if 'Average_Degree_less_than' in request.POST: #verifica se Degree_Centrality foi enviado na requisição
			Average_Degree_less_than = request.POST['Average_Degree_less_than']
			if Average_Degree_less_than:
				if  Average_Degree_less_than != "":
						texto = (""" FILTER( ?valorAverageDegree < """ + Average_Degree_less_than +") .")
						consulta+= ("?rede scnas:has_AverageDegree ?AverageDegree . ?AverageDegree SNAMetric:hasValue ?valorAverageDegree ." + texto)

		if 'Average_Degree_less_than' in request.POST: #verifica se Degree_Centrality foi enviado na requisição
			Average_Degree_less_than = request.POST['Average_Degree_less_than']
			if Average_Degree_less_than:
				if  Average_Degree_less_than != "":
						texto = (""" FILTER( ?valorAverageDegree < """ + Average_Degree_less_than +") .")
						consulta+= ("?rede scnas:has_AverageDegree ?AverageDegree . ?AverageDegree SNAMetric:hasValue ?valorAverageDegree ." + texto)


		if 'Average_Degree_greater_than' in request.POST: #verifica se Degree_Centrality foi enviado na requisição
			Average_Degree_greater_than = request.POST['Average_Degree_greater_than']
			if Average_Degree_greater_than:
				if  Average_Degree_greater_than != "":
						texto = (""" FILTER( ?valorAverageDegree > """ + Average_Degree_greater_than +") .")
						consulta+= (" ?rede scnas:has_AverageDegree ?AverageDegree . ?AverageDegree SNAMetric:hasValue ?valorAverageDegree . " + texto)

		if 'Component_less_than' in request.POST: #verifica se Degree_Centrality foi enviado na requisição
			Component_less_than = request.POST['Component_less_than']
			if Component_less_than:
				if  Component_less_than != "":
						texto = (""" FILTER( ?ValorComponent < """ + Component_less_than +") .")
						consulta+= (" ?rede SNAMetric:hasSNAMetricComponent ?Component . ?Component SNAMetric:hasValue ?ValorComponent . " + texto)

		if 'Component_greater_than' in request.POST: #verifica se Degree_Centrality foi enviado na requisição
			Component_greater_than = request.POST['Component_greater_than']
			if Component_greater_than:
				if  Component_greater_than != "":
						texto = (""" FILTER( ?ValorComponent > """ + Component_greater_than +") .")
						consulta+= (" ?rede SNAMetric:hasSNAMetricComponent ?Component . ?Component SNAMetric:hasValue ?ValorComponent . " + texto)

		if 'Density_less_than' in request.POST: #verifica se Degree_Centrality foi enviado na requisição
			Density_less_than = request.POST['Density_less_than']
			if Density_less_than:
				if  Density_less_than != "":
						texto = (""" FILTER( ?valorDensity < """ + Density_less_than +") .")
						consulta+= (" ?rede scnas:has_Density ?densidade . ?densidade SNAMetric:hasValue ?valorDensity . " + texto)

		if 'Density_greater_than' in request.POST: #verifica se Degree_Centrality foi enviado na requisição
			Density_greater_than = request.POST['Density_greater_than']
			if Density_greater_than:
				if  Density_greater_than != "":
						texto = (""" FILTER( ?valorDensity > """ + Density_greater_than +") .")
						consulta+= (" ?rede scnas:has_Density ?densidade . ?densidade SNAMetric:hasValue ?valorDensity . " + texto)

		if 'Region_Name' in request.POST: #verifica se Degree_Centrality foi enviado na requisição
			Region_Name = request.POST['Region_Name']
			if Region_Name:
				if  Region_Name != "":
						texto = (""" ?location SNAMetric:hasName '""" + Region_Name +"' .")
						consulta+= (" ?rede scnas:has_Location ?location . " + texto)			

		if 'Knowledge_Area_Name' in request.POST: #verifica se Degree_Centrality foi enviado na requisição
			Knowledge_Area_Name = request.POST['Knowledge_Area_Name']
			if Knowledge_Area_Name:
				if  Knowledge_Area_Name != "":
					texto = (""" ?type SNAMetric:hasName '""" + Knowledge_Area_Name +"' .")							
					consulta += (texto)		

		if 'Region' in request.POST: #verifica se Degree_Centrality foi enviado na requisição
 			Region = request.POST['Region']
 			if Region: 							
 				consulta += ("""
 				?assertion scnas:has_Network ?rede . 
				?type scnas:has_Location ?location.
				?location SNAMetric:hasName ?nomeLocation .""")
		if 'Degree_Centrality' in request.POST or 'Closeness_Centrality' in request.POST or 'Betweenness_Centrality' in request.POST:
			consulta += ("""  ?assertion scnas:has_Network ?rede .  """)
			Actor= "Actor"
			consulta += ("""
					?rede scnas:has_Actor ?actor.
 					?actor SNAMetric:hasName ?nameActor .""")
			if 'Degree_Centrality' in request.POST: #verifica se Degree_Centrality foi enviado na requisição
	 			Degree_Centrality = request.POST['Degree_Centrality']
	 			if Degree_Centrality:
	 				Degree = "Degree Centrality " 							
	 				consulta += ("""
					?actor SNAMetric:hasSNAMetricDegreeCentrality ?DegreeCentrality .
					?DegreeCentrality SNAMetric:hasValue ?valueDC .""")
			if 'Closeness_Centrality' in request.POST: #verifica se Closeness_Centrality foi enviado na requisição
				Closeness_Centrality = request.POST['Closeness_Centrality']
				if Closeness_Centrality:
					Closeness = "Closeness Centrality "							
					consulta += ("""
					?actor SNAMetric:hasSNAMetricClosenessCentrality ?ClosenessCentrality .
					?ClosenessCentrality SNAMetric:hasValue ?valueCC .""")
			if 'Betweenness_Centrality' in request.POST: #verifica se Betweenness_Centrality foi enviado na requisição
				Betweenness_Centrality = request.POST['Betweenness_Centrality']
				if Betweenness_Centrality:
					Betweenness = "Betweenness Centrality "						
					consulta += ("""
					?actor SNAMetric:hasSNAMetricBetweennessCentrality ?BetweennessCentrality .
					?BetweennessCentrality SNAMetric:hasValue ?valueBC .""")

		if 'Density' in request.POST or 'Component' in request.POST or 	'Average_Degree' in request.POST or 'Actors_Number' in request.POST or 'Edges_Number' in request.POST:
			consulta+=(" ?assertion scnas:has_Network ?rede .")
			if 'Density' in request.POST: #verifica se Degree_Centrality foi enviado na requisição
	 			Density = request.POST['Density']
	 			if Density:
	 				Density_ = "Density"
	 				consulta += ("""
					?rede scnas:has_Density ?densidade .
		 			?densidade SNAMetric:hasValue ?valorDensity .""") 
			if 'Component' in request.POST: #verifica se Degree_Centrality foi enviado na requisição
	 			Component = request.POST['Component']
	 			if Component:
	 				consulta += ("""
					?rede SNAMetric:hasSNAMetricComponent ?Component .
	 				?Component SNAMetric:hasValue ?ValorComponent. """) 
			if 'Average_Degree' in request.POST: #verifica se Degree_Centrality foi enviado na requisição
	 			Average_Degree = request.POST['Average_Degree']
	 			if Average_Degree:
	 				consulta += ("""
					?rede scnas:has_AverageDegree ?AverageDegree .
					 ?AverageDegree SNAMetric:hasValue ?valorAverageDegree .""") 
			if 'Actors_Number' in request.POST: #verifica se Degree_Centrality foi enviado na requisição
	 			Actors_Number = request.POST['Actors_Number']
	 			if Actors_Number:
	 				consulta += ("""
					?rede scnas:has_ActorsNumber ?ActorsNumber .
	 				?ActorsNumber SNAMetric:hasValue ?ValueActorsNumber .""")
			if 'Edges_Number' in request.POST: #verifica se Degree_Centrality foi enviado na requisição
	 			Edges_Number = request.POST['Edges_Number']
	 			if Edges_Number:
	 				consulta += ("""
					?rede scnas:has_EdgesNumber ?EdgesNumber .
					?EdgesNumber SNAMetric:hasValue ?ValueEdgesNumber .""")


		consulta += ("""
		}
		LIMIT 10000""")

		sparql.setQuery(consulta)
		sparql.setReturnFormat(JSON)
		results = sparql.query().convert()
		Titles = "No"
		listaresultados=[]


		def remove_repetidos(lista):
		    l = []
		    for i in lista:
		        if i not in l:
		            l.append(i)
		    l.sort()
		    return l

		for result in results["results"]["bindings"]:
			for var in results["head"]["vars"]:	
				if var == "anoinicio":
					Inicio = "Inicio"
					listaAnoInicio.append(result[var]['value'])
				if var == "anofim":
					Fim = "Fim"
					listaAnoFim.append(result[var]['value'])			
				if var == "title":
					Titles = "SCNAS"
					listaTitulos.append(result[var]['value'])
					aux= remove_repetidos(listaTitulos)
					counttitles= len(aux)
				if var == "URL":
					DOI= "DOI"
					listaURL.append(result[var]['value'])
				if var == "nomeLocation":
					Location = "Location"
					listaRegion.append(result[var]['value'])
				if var == "nameType":
					AC= "Knowledge Area"
					listaAC.append(result[var]['value'])				
				if 'Degree_Centrality' in request.POST or 'Closeness_Centrality' in request.POST or 'Betweenness_Centrality' in request.POST:
					if var == "nameActor":
						listaActor.append(result[var]['value'])
					if 'Degree_Centrality' in request.POST: #verifica se Degree_Centrality foi enviado na requisição
			 			Degree_Centrality = request.POST['Degree_Centrality']
			 			if Degree_Centrality:
			 				if var == "valueDC":
			 					listaDC.append(result[var]['value'])
					if 'Closeness_Centrality' in request.POST: #verifica se Closeness_Centrality foi enviado na requisição
						Closeness_Centrality = request.POST['Closeness_Centrality']
						if Closeness_Centrality:
							if var == "valueCC":
								listaCC.append(result[var]['value'])
					if 'Betweenness_Centrality' in request.POST: #verifica se Betweenness_Centrality foi enviado na requisição
						Betweenness_Centrality = request.POST['Betweenness_Centrality']
						if Betweenness_Centrality:
							if var == "valueBC":
								listaBC.append(result[var]['value'])
				if 'Density' in request.POST or 'Component' in request.POST or 'Average_Degree' in request.POST or 'Actors_Number' in request.POST or 'Edges_Number' in request.POST:					

					if 'Density' in request.POST: #verifica se Betweenness_Centrality foi enviado na requisição
						Densidade= "Density"
						Density = request.POST['Density']
						if Density:
							if var == "valorDensity":
								listaDensity.append(result[var]['value'])
					if 'Component' in request.POST: #verifica se Betweenness_Centrality foi enviado na requisição
						Compo="Component"
						Component = request.POST['Component']
						if Component:
							if var == "ValorComponent":
								listaComponentes.append(result[var]['value'])
					if 'Average_Degree' in request.POST: #verifica se Betweenness_Centrality foi enviado na requisição
						Average_Degree = request.POST['Average_Degree']
						if Average_Degree:
							Average= "Average Degree"
							if var == "valorAverageDegree":
								listaAverageDegree.append(result[var]['value'])
					if 'Actors_Number' in request.POST: #verifica se Betweenness_Centrality foi enviado na requisição
						Actors_Number = request.POST['Actors_Number']
						if Actors_Number:
							AN= "Actors Number"
							if var == "ValueActorsNumber":
								listaActorsNumber.append(result[var]['value'])

					if 'Edges_Number' in request.POST: #verifica se Betweenness_Centrality foi enviado na requisição
						Edges_Number = request.POST['Edges_Number']
						if Edges_Number:
							EN= "Edges Number"
							if var == "ValueEdgesNumber":
								listaEdgesNumber.append(result[var]['value'])


	return render(request, "Geographic.html", {'GeographicOther':GeographicOther, 'ActorMetrics': ActorMetrics, 'NetworkMetrics': NetworkMetrics, 'FiltroGeographic':FiltroGeographic, 'filtroNetworkMetrics': filtroNetworkMetrics, 'filtroActorsMetrics': filtroActorsMetrics, 'Atores': listaActor, 'DCs':listaDC, 'CCs':listaCC, 'BCs': listaBC, 'URLs': listaURL, 'Titulos': listaTitle, 'Densities': listaDensity, 'Componentes': listaComponentes, 'AverageDegrees': listaAverageDegree, "Regions": listaRegion, 
	'Location': Location, 'Betweenness': Betweenness, 'Closeness': Closeness, 'Degree': Degree, 'DOI': DOI, 'Locations': ListaLocation, 'Actor': Actor, 'Densidade':Densidade, 'titulo': titulo, 'Compo':Compo, 'Averag': Average, 'numerodeatores': listaActorsNumber, 'AN':AN, 'EN':EN, "numerodeedges": listaEdgesNumber, "AC": AC, "listaAC": listaAC, 'listaTitles': listaTitulos, "Titles":Titles, "counttitles":counttitles, 'listaAnoFim':listaAnoFim, 'listaAnoInicio':listaAnoInicio,'Inicio':Inicio, 'Fim': Fim })
	