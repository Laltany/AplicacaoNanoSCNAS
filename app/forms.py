from django import forms


class other(forms.Form):
	# For BooleanFields, required=False means that Django's validation
	# will accept a checked or unchecked value, while required=True
	# will validate that the user MUST check the box
	Region = forms.BooleanField(required=False)
	Network_Time = forms.BooleanField(required=False)
	Knowledge_Area = forms.BooleanField(required=False)
	Actors_Number = forms.BooleanField(required=False)
	Edges_Number = forms.BooleanField(required=False)


class ActorMetrics(forms.Form):
	Degree_Centrality = forms.BooleanField(required=False)
	Closeness_Centrality = forms.BooleanField(required=False)
	Betweenness_Centrality = forms.BooleanField(required=False)

class NetworkMetrics(forms.Form):
	Density = forms.BooleanField(required=False)
	Component = forms.BooleanField(required=False)
	Average_Degree = forms.BooleanField(required=False)

class filtroKnowledgeArea(forms.Form):
	Knowledge_Area_Name = forms.CharField(required=False)
	Region_Name = forms.CharField(required=False)
	Network_Time_Begginning = forms.CharField(required=False)
	Network_Time_End = forms.CharField(required=False)

class filtroNetworkMetrics(forms.Form):	
	Density_greater_than = forms.CharField(required=False)
	Density_less_than=  forms.CharField(required=False)
	Component_greater_than = forms.CharField(required=False)
	Component_less_than=  forms.CharField(required=False)
	Average_Degree_greater_than = forms.CharField(required=False)
	Average_Degree_less_than=  forms.CharField(required=False)

class filtroActorsMetrics(forms.Form):	
	Degree_Centrality_greater_than = forms.CharField(required=False)
	Degree_Centrality_less_than=  forms.CharField(required=False)
	Closeness_Centrality_greater_than = forms.CharField(required=False)
	Closeness_Centrality_less_than=  forms.CharField(required=False)
	Betweenness_Centrality_greater_than = forms.CharField(required=False)
	Betweenness_Centrality_less_than=  forms.CharField(required=False)

class PeriodicOther(forms.Form):
	Knowledge_Area = forms.BooleanField(required=False)
	Network_Time = forms.BooleanField(required=False)
	Actors_Number = forms.BooleanField(required=False)
	Edges_Number = forms.BooleanField(required=False)

class filtroPeriodic(forms.Form):
	Knowledge_Area_Name = forms.CharField(required=False)
	Periodic_Name = forms.CharField(required=False)
	Network_Time_Begginning = forms.CharField(required=False)
	Network_Time_End = forms.CharField(required=False)


class EventOther(forms.Form):
	Knowledge_Area = forms.BooleanField(required=False)
	Network_Time = forms.BooleanField(required=False)
	Actors_Number = forms.BooleanField(required=False)
	Edges_Number = forms.BooleanField(required=False)	

class filtroEvent(forms.Form):
	Knowledge_Area_Name = forms.CharField(required=False)
	Event_Name = forms.CharField(required=False)
	Network_Time_Begginning = forms.CharField(required=False)
	Network_Time_End = forms.CharField(required=False)

class InstitutionOther(forms.Form):
	High_Education_Institution = forms.BooleanField(required=False)
	Region = forms.BooleanField(required=False)
	Network_Time = forms.BooleanField(required=False)
	Actors_Number = forms.BooleanField(required=False)
	Edges_Number = forms.BooleanField(required=False)	

class filtroInstitution(forms.Form):
	High_Education_Institution_Name = forms.CharField(required=False)
	Region_Name = forms.CharField(required=False)
	Network_Time_Begginning = forms.CharField(required=False)
	Network_Time_End = forms.CharField(required=False)

class PGPOther(forms.Form):
	Knowledge_Area = forms.BooleanField(required=False)
	HEI = forms.BooleanField(required=False)
	Region = forms.BooleanField(required=False)
	Network_Time = forms.BooleanField(required=False)
	Actors_Number = forms.BooleanField(required=False)
	Edges_Number = forms.BooleanField(required=False)	

class FiltroPGP(forms.Form):
	Knowledge_Area_Name = forms.CharField(required=False)
	HEI_Name = forms.CharField(required=False)
	Region_Name= forms.CharField(required=False)
	Network_Time_Begginning = forms.CharField(required=False)
	Network_Time_End = forms.CharField(required=False)


class GeographicOther(forms.Form):
	Region = forms.BooleanField(required=False)
	Network_Time = forms.BooleanField(required=False)
	Actors_Number = forms.BooleanField(required=False)
	Edges_Number = forms.BooleanField(required=False)	

class FiltroGeographic(forms.Form):
	Region_Name= forms.CharField(required=False)
	Network_Time_Begginning = forms.CharField(required=False)
	Network_Time_End = forms.CharField(required=False)