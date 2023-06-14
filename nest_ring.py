import nest
import nest.voltage_trace
import matplotlib.pyplot as plt
%matplotlib inline
nest.set_verbosity("M_WARNING")
nest.ResetKernel()

ncells = 4
weight = 200 # ??
delay = 5    # ms ?

nest.resolution = 0.01 # must be set before creating other Nest objects.

# https://nest-simulator.readthedocs.io/en/v3.4/models/iaf_psc_alpha.html
# does not desribe defaults, with which no AP propagates. Values taken from nest example
nest.SetDefaults("iaf_psc_alpha", #
{"C_m": 10.0,
"tau_m": 15.58,
"t_ref": 2.0,
"E_L": -65.0,
"V_th": -40.0,
"V_reset": -65.0})
# nest.SetDefaults("iaf_psc_alpha", #taken from Arbor LIF cell
# {"C_m": 20,
# "tau_m": 10,
# "t_ref": 2,
# "E_L": 0,
# "V_th": 10,
# "V_reset": 9.9,
# "V_m": 10})

neurons  = nest.Create("iaf_psc_alpha",ncells)

# https://nest-simulator.readthedocs.io/en/v3.0/guides/connection_management.html#synapse-spec
# does not mention units for syn_spec parameters.
network = [nest.Connect(neurons[i], neurons[(i+1)%ncells], syn_spec={"weight": weight, "delay": delay}) for i in range(ncells)]

voltmeter = nest.Create("voltmeter")
voltmeters = [nest.Connect(voltmeter, neurons[i]) for i in range(ncells)]

spike_gen = nest.Create("spike_generator", params={"spike_times": [1]})

nest.Connect(spike_gen, neurons[0], syn_spec={"weight": weight})
nest.Simulate(150)

nest.voltage_trace.from_device(voltmeter)
plt.show()