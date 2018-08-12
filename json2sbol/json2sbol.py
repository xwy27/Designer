# data: {
#   components: [{
#     'role': xxx,
#     'id': xxx,
#     'name': xxx,
#     'version': xxx,
#     'description': xxx,
#     'sequence': xxx
#   }],
#   lines: [
#     [xxx, xxx, xxx]
#   ],
#   promotions: [{
#     'stimulator': xxx, # id of the promotor
#     'other': xxx # id of the material promoted
#   }],
#   inhibitions: [{
#     'inhibitor': xxx, # id of the promotor
#     'other': xxx # id of the material promoted
#   }],
#   combines: [{
#     'x': xxx, # id of the combination
#     'y': xxx,
#     'z': xxx,
#     'production': xxx # id of the production
#   }],
#   circuit: {
#     'id': xxx, # circuit id if it's already existing, -1 else
#     'name': xxx,
#     'description': xxx
#   }
# }

# import request
import json
from sbol import *

setHomespace('http://sys-bio.org')
doc = Document()

roles = {
  'DNA': SO_GENE,
  'PRO': SO_PROMOTER,
  'RBS': SO_RBS,
  'CDS': SO_CDS,
  'TER': SO_TERMINATOR,
  'RNA': SO_SGRNA
}

# data = json.loads(request.POST['data'])

test = '{"components":[{"role":"PRO","id":"I14032","name":"I14032","version":1,"description":"test","sequence":"atcg"},{"role":"CDS","id":"I14031","name":"I14031","version":1,"description":"test","sequence":"atcg"},{"role":"TER","id":"I14030","name":"I14030","version":1,"description":"test","sequence":"atcg"}],"lines":[["I14032","I14031","I14030"]],"circuit":{"id":1,"name":"test_gene","description":"test circuit"},"promotions":[{"stimulator":"I14032","other":"I14031"},{"stimulator":"I14030","other":"I14031"}],"inhibitions":[{"inhibitor":"I14031","other":"I14032"},{"inhibitor":"I14031","other":"I14030"}]}'
data = json.loads(test)

# load components
components = {}
for component in data['components']:
  temp = ComponentDefinition(component['id'])
  temp.role = roles[component['role']]
  temp.description = component['description']
  temp.sequence = Sequence(component['id'], component['sequence'])
  components[component['id']] = temp
  doc.addComponentDefinition(temp)

circuit = ComponentDefinition(data['circuit']['name'])
circuit.description = data['circuit']['description']
doc.addComponentDefinition(circuit)

# load circuit structure
structure = []
for line in data['lines']:
  for temp in line:
    structure.append(components[temp])

circuit.assemblePrimaryStructure(structure)

# functional components
pro_fcs = {}
inh_fcs = {}

# promotion
proModule = ModuleDefinition('promotion_module')
doc.addModuleDefinition(proModule)

for promotion in data['promotions']:
  stimulatorName = promotion['stimulator']
  otherName = promotion['other']
  
  if ((stimulatorName in pro_fcs.keys()) == False):
    stimulator_fc = proModule.functionalComponents.create(stimulatorName)
    stimulator_fc.definition = components[stimulatorName].identity
    stimulator_fc.access = SBOL_ACCESS_PUBLIC
    stimulator_fc.direction = SBOL_DIRECTION_IN_OUT
    pro_fcs[stimulatorName] = stimulator_fc

  if ((otherName in pro_fcs.keys()) == False):
    other_fc = proModule.functionalComponents.create(otherName)
    other_fc.definition = components[otherName].identity
    other_fc.access = SBOL_ACCESS_PUBLIC
    other_fc.direction = SBOL_DIRECTION_IN_OUT
    pro_fcs[otherName] = other_fc

  proInteraction = proModule.interactions.create(stimulatorName + '_' + otherName + '_promotion')
  proInteraction.types = SBO_STIMULATION

  stimulator_participation = proInteraction.participations.create(stimulatorName)
  stimulator_participation.roles = SBO_STIMULATOR
  stimulator_participation.participant = pro_fcs[stimulatorName].identity

  other_participation = proInteraction.participations.create(otherName)
  other_participation.roles = components[otherName].role
  other_participation.participant = pro_fcs[otherName].identity

# inhibition
inhModule = ModuleDefinition('inhbition_module')
doc.addModuleDefinition(inhModule)

for inhibition in data['inhibitions']:
  inhibitorName = inhibition['inhibitor']
  otherName = inhibition['other']
  
  if ((inhibitorName in inh_fcs.keys()) == False):
    inhibitor_fc = inhModule.functionalComponents.create(inhibitorName)
    inhibitor_fc.definition = components[inhibitorName].identity
    inhibitor_fc.access = SBOL_ACCESS_PUBLIC
    inhibitor_fc.direction = SBOL_DIRECTION_IN_OUT
    inh_fcs[inhibitorName] = inhibitor_fc

  if ((otherName in inh_fcs.keys()) == False):
    other_fc = inhModule.functionalComponents.create(otherName)
    other_fc.definition = components[otherName].identity
    other_fc.access = SBOL_ACCESS_PUBLIC
    other_fc.direction = SBOL_DIRECTION_IN_OUT
    inh_fcs[otherName] = other_fc

  inhInteraction = inhModule.interactions.create(inhibitorName + '_' + otherName + '_inhibition')
  inhInteraction.types = SBO_INHIBITION

  inhibitor_participation = inhInteraction.participations.create(inhibitorName)
  inhibitor_participation.roles = SBO_INHIBITOR
  inhibitor_participation.participant = inh_fcs[inhibitorName].identity

  other_participation = inhInteraction.participations.create(otherName)
  other_participation.roles = components[otherName].role
  other_participation.participant = inh_fcs[otherName].identity

# create sbol document
circuit_name = data['circuit']['name']
result = doc.write(circuit_name + '.xml')
print(result)