<template>

  <!--{{projectdata.some((n) => n) === true}}
  <div v-if="projectdata.some((n) => n) === true">
    <Function :id="projectdata[0].id" :parentId="projectdata[0].parentId" :nodes="nodes" :node="nodes[0]"/>
  </div>
  <div v-else>

   </div>-->

  <div v-for="(node, networkId) in projectdata.filter((n) => !n.parentInput)">
    <table>
      <tr>
        <td align="left"><!-- Network: {{ networkId + 1 }} --></td>
        <td></td>
        <td></td>
      </tr>
      <tr>
        <td>
          <Function
            :id="node.id"
            :networkId="networkId + 1"
            :projectdata="projectdata"
			:enableEdit="enableEdit[statusdata.state]"
			:isInMonitorMode="monitorTaskStart[statusdata.monitor]"
            :node="projectdata.filter((n) => n.id === node.id)[0]"
            :variables="variablesdata"
            :interConnection="interConnection"
            :interConnectionDetails="interConnectionDetails"
            @new-variable="
              (event) => {
                addNewVarIfNotExisting(
                  event.node,
                  event.mem_loc,
                  event.output_type
                );
				//putProjectDataToFlask();
			}"
          />
        </td>
        <td width="20px" valign="top">
          <hr />
        </td>
        <td valign="top">
          <button
			v-if="enableEdit[statusdata.state]"
            :class="
              interConnection && interConnectionDetails.nodeId === node.id
                ? 'button button-red'
                : 'button button-gray'
            "
            @click.stop="
              interConnection = true;
              interConnectionDetails.nodeId = node.id;
              interConnectionDetails.networkId = networkId + 1;
              interConnectionDetails.outputType = node.output_type;
            "
          >
            [
          </button>
          <div
            v-if="interConnection === true"
            v-click-outside="diselectInterConnection"
          ></div>
        </td>
      </tr>
    </table>
  </div>

  <div align="left" v-if="enableEdit[statusdata.state]">
    <FunctionList
      @selected="
        addChild(Date.now(), null, $event);
        forceFunctionListRerender();
      "
      :key="functionListKey"
      :outputType="['any']"
      :alone="true"
    />
  </div>

  <br />

  <table class="mem_table" width="60%">
    <tr>
      <th>Address</th>
      <th>Type</th>
      <th>Description</th>
      <th>References</th>
	  <th v-if="monitorTaskStart[statusdata.monitor]">Process Value</th>
	  <th v-if="enableEdit[statusdata.state]">Action</th>
      <th v-if="monitorTaskStart[statusdata.monitor]">Forced</th>
	  <th v-if="monitorTaskStart[statusdata.monitor]">Forced value</th>
    </tr>

    <template v-for="variable in variablesdata">
      <tr v-if="variable.monitor === true">
        <td>{{ variable.name }}</td>
        <td>{{ variable.type }}</td>
        <td>
          <div
            v-if="variable.edit === false"
            style="background-color: transparent"
            @click="
              variable.edit = enableEdit[statusdata.state];
            "
          >
            {{ variable.description }}&nbsp
          </div>
		  <VarInput 
			v-if="variable.edit === true"
			:value="variable.description"
			v-on:blur="variable.edit = false"
            @enter="variable.edit = false;"
			@valueChanged="(value) => {variable.description = value; putVariableDataToFlask();}"
		  />
          <!--<input
            ref="desc_input"
            v-if="variable.edit === true"
            :value="variable.description"
            @input="
              (event) => {
                variable.description = event.target.value;
              }
            "
            v-on:blur="variable.edit = false"
            @keyup.enter="variable.edit = false"
          />-->
        </td>
        <td>
          {{
            projectdata.filter(
              (n) =>
                n.mem_loc === variable.name /*&& n.mem_input.some((m) => m === variable.type)*/
            ).length
          }}
        </td>
		<td v-if="monitorTaskStart[statusdata.monitor]">
			{{variable.value}}
		</td>
        <td align="center" v-if="enableEdit[statusdata.state]">
		  <table>
		  <tr>
		  <td>
          <button 
			v-if="enableEdit[statusdata.state]"
            class="button button-red"
            @click="deleteVariable(variable.id)"
          >
            X
          </button>
		  </td>
		  </tr>
		  </table>
        </td>
		<td v-if="monitorTaskStart[statusdata.monitor]">
			<input type="checkbox" id="forced" :checked="variable.forced === true" v-on:input="toggleForceVariable(variable.id);"/>
		</td>
		<td v-if="monitorTaskStart[statusdata.monitor]">
			<input type="checkbox" id="forcedValue" :checked="variable.forcedValue === 1" v-on:input="toggleForceVariableValueBool(variable.id);"/>
		</td>
      </tr>
    </template>
  </table>

  <div v-set="(varName = '???')"></div>
  <select
	v-if="enableEdit[statusdata.state]"
    v-model="selected"
    @change="
      varName = inputDialog('Enter variable name: ');
      if (
        varName.match(
          varTypes.filter((md) => md.type === $event.target.value)[0].valid
        )
      ) {
        addNewVarIfNotExisting(null, varName, $event.target.value);
      } else {
        showAlert('Wrong name for that data type!');
      }
      selected = 'undefined';
    "
  >
    <option
      disabled="disabled"
      value="undefined"
      selected="true"
      align="center"
    >
      +
    </option>
    <template v-for="t in varTypes">
      <option :value="t.type">{{ t.type }}</option>
    </template>
  </select>

  <br />
  <br />

  <table>
    <tr>
      <td>
        <!--<textarea cols="30" rows="20">{{ projectdata }}</textarea>-->
      </td>
      <td>
         <!--<textarea cols="30" rows="20">{{ listing }}</textarea>-->
        <button
		  v-if="compileButtonVisible[statusdata.changed]"
          @click="
            listing.splice(0);
            buildListing(projectdata);
			putCompileDataToFlask();
          "
		  :disabled="!isProgramDataReadyToCompile(projectdata, varTypes)"
        >
		
          Compile
        </button>
		<button
		  v-if="stopButtonVisible[statusdata.state]"
          @click="axios.get(flaskURL+'/stop')
					.then((res) => {
						statusdata = res.data;
						console.log(res.data);
						
						delay(() => {
							getProjectDataFromFlask();
							delay(() => clearMonitorValues(), 500); 
							}, 500);
					})
					.catch((err) => console.error(err)); /* getVariableDataFromFlask();getProjectDataFromFlask();*/"
        >
          Stop
        </button>
		<button
		  v-if="startButtonVisible[statusdata.state] && !compileButtonVisible[statusdata.changed]"
          @click="axios.get(flaskURL+'/start')
					.then((res) => {statusdata = res.data;})
					.catch((err) => console.error(err)); /*getVariableDataFromFlask();getProjectDataFromFlask();*/"
        >
          Start
        </button>
		<div v-if="monitorCheckboxVisible[statusdata.state]">
			<input type="checkbox" id="monitor" :checked="statusdata['monitor'] == 'on'" v-on:input="toggleMonitorFromFlask();"/>
			<label for="monitor">Monitor</label>
		</div>
      </td>
	  <td>
		<div>&nbspStatus: {{statusdata}} </div>
	  </td>
      <td>
         <!--<textarea cols="30" rows="20">{{ variablesdata }}</textarea>-->
      </td>
    </tr>
  </table>
 <!--{{ interConnectionDetails }}-->

</template>

<script setup>
import axios from "axios";
import definitions from "./assets/definitions.json";
import varTypes from "./assets/var-types.json";
import Function from "./components/Function.vue";
import FunctionList from "./components/FunctionList.vue";
import FunctionListing from "./components/FunctionListing.vue";
import VarInput from "./components/VarInput.vue";
import { ref, provide, onMounted, onUpdated, onUnmounted } from "vue";

const statusdata = ref([]);
const projectdata = ref([]);
const compiledata = ref([]);
const setuplisting = ref([]);
const listing = ref([]);
const variablesdata = ref([]);
//const flaskURL = "http://192.168.1.2"
const flaskURL = "http://localhost:5000"
//const varTypes = ref(variableTypes);

const enableEdit = {"stopped" : true, "running" : false}
const stopButtonVisible = {"stopped" : false, "running" : true}
const startButtonVisible = {"stopped" : true, "running" : false}
const compileButtonVisible = {"changed" : true, "not changed" : false}
const monitorCheckboxVisible = {"stopped" : false, "running" : true}
const monitorTaskStart = {"on" : true, "off" : false}

var monitorInterval = null

const interConnection = ref(false);
const interConnectionDetails = ref({
  nodeId: 0,
  networkId: -1,
  outputType: ["any"],
});

function diselectInterConnection() {
  interConnection.value = false;
}

const recursiveLoopBasedOnInputs = (data, element, inputId) => {
  if (element) {
    listing.value.push({
      functionName:
        "before_" + (element.alias != "" ? element.alias : element.block),
      memoryAddr: element.mem_loc !== "???" ? element.mem_loc : undefined,
      id: element.id.toString(),
	  //destInputId: inputId !== null ? inputId.toString() : "", 
    });

    Array.prototype.forEach.call(element.inputs, (input) => {
      var nestedElement = data.filter((e) => e.id === input.target)[0];
      var funcName = element.alias != "" ? element.alias : element.block;

      listing.value.push({
        functionName: "before_" + funcName + "_INPUT",
        inputName: input.name,
        memoryAddr: element.mem_loc !== "???" ? element.mem_loc : undefined,
        id: element.id.toString(),
        connNodeId: nestedElement.id.toString(),
      });

      recursiveLoopBasedOnInputs(data, nestedElement, input.id);

      listing.value.push({
        functionName: "after_" + funcName + "_INPUT",
        inputName: input.name,
		memoryAddr: element.mem_loc !== "???" ? element.mem_loc : undefined,
        id: element.id.toString(),
        connNodeId: nestedElement.id.toString(),
      });
    });

    listing.value.push({
      functionName:
        "after_" + (element.alias != "" ? element.alias : element.block),
      memoryAddr: element.mem_loc !== "???" ? element.mem_loc : undefined,
      id: element.id.toString(),
	  //destInputId: inputId !== null ? inputId.toString() : ""
    });
  }
};

const buildListing = (data) => {
	
  setuplisting.value = [];
  listing.value = [];
  //setup listing
  data.forEach((element) => {
      setuplisting.value.push({
        functionName: "setup_" + (element.alias != "" ? element.alias : element.block),
        inputName: element.name,
        memoryAddr: element.mem_loc !== "???" ? element.mem_loc : undefined,
        id: element.id.toString(),
      });
  });
  //program listing
  data.forEach((element) => {
    if (element.parentInput === null) {
      //listing.value.push({ function: "CANCEL_RLO" });
      recursiveLoopBasedOnInputs(data, element, null, undefined);
    }
  });

  compiledata.value.push({setuplisting: setuplisting, listing: listing});
  console.log(compiledata.value);

};

const checkIfVariableExists = (name) => {
  return variablesdata.value.filter((v) => v.name === name)[0];
};

const addNewVarIfNotExisting = (node, name, type) => {
  var found = checkIfVariableExists(name);
  var monitor = varTypes.filter((t) => type === t.type)[0].monitor
  if (!found) {
	  if(monitor === true){
		var newVar = {
		  id: Date.now(),
		  name: name,
		  type: type,
		  description: "",
		  edit: false,
		  value: 0,
		  forced: false,
		  forcedValue: 0,
		  monitorData: 0,
		  monitor: monitor
		};
		variablesdata.value.push(newVar);
		putProjectDataToFlask();
		return;
	  }
	  return;
  }
  putProjectDataToFlask();
};

const deleteVariable = (id) => {
  var varName = variablesdata.value.filter((v) => v.id === id)[0].name;
  variablesdata.value = variablesdata.value.filter((v) => v.id != id);
  projectdata.value.forEach((node) => {
    if (node.mem_loc === varName) {
      node.mem_loc = "???";
    }
  });
  putProjectDataToFlask();
};

const toggleForceVariable = (id) => {
  var variable = variablesdata.value.filter((v) => v.id === id)[0];
  variable.forced = !variable.forced;
  if(variable.forced === true) variable.forcedValue = 0;
  postForceVariables();
};

const toggleForceVariableValueBool = (id) => {
  var variable = variablesdata.value.filter((v) => v.id === id)[0];
  if(variable.forcedValue === 1){
	variable.forcedValue = 0; 
  }else{
    variable.forcedValue = 1;
  }
  postForceVariables();
};

const setForcedValueOfVariable = (id, val) => {
  var variable = variablesdata.value.filter((v) => v.id === id)[0];
  variable.forcedValue = val;
  putProjectDataToFlask();
};

const toggleForcedValueOfVariable = (id, val) => {
  var variable = variablesdata.value.filter((v) => v.id === id)[0];
  variable.forcedValue = val;
  putProjectDataToFlask();
};

const getStatusDataFromFlask = () => {
  const path = flaskURL+"/status";
	axios.get(path).then((res) => {console.log(res.data);statusdata.value = res.data;})
		.catch((err) => console.error(err));
}

const clearMonitorValues = () => {
  projectdata.value.forEach((node) => {
    node.value = 0
    if (node.inputs) {
      node.inputs.forEach((input) => {
          input.value = 0;
      });
    }
  });
}

const toggleMonitorFromFlask = () => {
  clearMonitorValues();
  const path = flaskURL+"/monitor";
	axios.get(path).then((res) => {
			console.log(res.data);
			statusdata.value = res.data;
		})
		.catch((err) => console.error(err));
}

/*const getVariableDataFromFlask = () => {
  const path = flaskURL+"/variables";
	axios.get(path).then((res) => {
		console.log(res.data);
		variablesdata.value = res.data.variablesdata;
		statusdata.value = res.data.statusdata
	}).catch((err) => console.error(err));
}*/

/*const putVariableDataToFlask = () => {
  const path = flaskURL+"/variables";
  axios.post(path, variablesdata.value)
        .then((res) => {
			statusdata.value = res.data.statusdata
        }).catch((err) => console.error(err));
}*/

const getProjectDataFromFlask = () => {
  const path = flaskURL+"/project";
	axios.get(path).then((res) => {
			//console.log(res.data.project.program);
			projectdata.value = res.data.project.program;
			//console.log(projectdata.value);
			variablesdata.value = res.data.project.variables;
			statusdata.value = res.data.statusdata;
		})
		.catch((err) => console.error(err));
}

const putProjectDataToFlask = () => {
  const path = flaskURL+"/project";
  axios.post(path, {program: projectdata.value, variables: variablesdata.value, checksum: statusdata.value.checksum})
        .then((res) => {
			if(res.data.checksum == "bad")
				alert("Integrity error! Please reload page (F5)");
			else
				statusdata.value = res.data.statusdata;
        }).catch((err) => console.error(err));
}

const putCompileDataToFlask = () => {
  const path = flaskURL+"/compile";
  axios.post(path, compiledata.value).then((res) => {statusdata.value = res.data.statusdata;}).catch((err) => console.error(err));
}

const pullRuntimeData = () => {
  const path = flaskURL+"/pullruntimedata";
	axios.get(path).then((res) => {
			console.log(res.data);
			projectdata.value = res.data.project.program;
			variablesdata.value = res.data.project.variables;
			//variablesdata.value = res.data.variablesdata;
			//projectdata.value = res.data.projectdata;
			statusdata.value = res.data.statusdata;
		})
		.catch((err) => console.error(err));
}

const postForceVariables = () => {
  const path = flaskURL+"/forcevariables";
  axios.post(path, variablesdata.value)
        .then((res) => {
			statusdata.value = res.data.statusdata;
        }).catch((err) => console.error(err));
}

onMounted(() => {

  //getVariableDataFromFlask();
  getProjectDataFromFlask();

  monitorInterval = setInterval(() => {
	if(monitorTaskStart[statusdata.value.monitor]){
		pullRuntimeData();
	}
  }, 500);

  //getStatusDataFromFlask();
})

onUpdated(() => {
});

onUnmounted(() => {
	clearInterval(monitorInterval)
});

const addChild = (id, parentInput, blockJson) => {
  var parentId = null;
  var block = JSON.parse(blockJson);
  var inputs = [];
  var inputCounter = 0;
  if (parentInput) {
    parentId = parentInput.id;
    parentInput.target = id;
  }

  projectdata.value.push({
    parentInput: parentId,
    id: id,
    inputs: inputs,
    block: block.name,
    alias: block.alias,
    description: "",
    mem_edit: false,
    mem_loc: block.mem_loc,
    mem_input: block.mem_input,
    dyn_inputs: block.dyn_inputs,
    output_type: block.output_type,
    dyn_inputs_type: block.dyn_inputs_type,
    input_only: block.input_only,
    networkId: -1,
    header_hover: false,
    value: 0,
  });

  /*definitions.forEach((group) => {
    group.blocks.forEach((def) => {
      if (def.name === block.name && !def.dyn_inputs && def.inputs) {
        def.inputs.forEach((inputDef) => {
          addInput(id, inputDef, inputCounter);
          inputCounter++;
        });
      }
    });
  });*/
  definitions.forEach((group) => {
    group.blocks.forEach((def) => {
      if (def.name === block.name && !def.dyn_inputs && def.inputs) {
        def.inputs.forEach((inputDef) => {
          setTimeout(() => {
            addInput(id, inputDef, inputCounter);
            inputCounter++;
          }, 10);
        });
      }
    });
  });

  putProjectDataToFlask();
};
const addInput = (nodeId, inputDef, idOffset = 0) => {
  // var inputJson = JSON.parse(input /*? input : '{"name":"", "type":"none"}'*/);
  let found = projectdata.value.filter((item) => item.id === nodeId);

  found.forEach((element) => {
	//console.log(element);
    element.inputs.push({
      id: Date.now() + idOffset,
      target: -1,
      name: inputDef.name,
      type: inputDef.type,
      conn_mouse_hover: false,
      input_mouse_hover: false,
      show_name: inputDef.show_name,
      value: 0,
    });
  });
  //putProjectDataToFlask();
};

const connectNodeToInput = (nodeId, inputId) => {
  //alert(nodeId + ", " + inputId);
  projectdata.value.forEach((node) => {
    if (node.id === nodeId) node.parentInput = inputId;
    if (node.inputs) {
      node.inputs.forEach((input) => {
        if (input.id === inputId) {
          input.target = nodeId;
          //input.type = node.output_type;
          //alert("input.id=" + input.id + "?=" + inputId);
        }
      });
    }
  });
  putProjectDataToFlask();
};

const disconnectNodeFromInput = (nodeId, inputId) => {
  //alert(nodeId + ", " + inputId);
  var isInputOnly = false;
  projectdata.value.forEach((node) => {
    if (node.id === nodeId) {
      node.parentInput = null;
      if (node.input_only === true) {
        deleteChild(node.id);
      }
    }
    if (node.inputs) {
      node.inputs.forEach((input) => {
        if (input.id === inputId) {
          input.target = -1;
        }
      });
    }
  });
  putProjectDataToFlask();
};

const clearInput = (inputId) => {};

const deleteInput = (inputId) => {
  var found = projectdata.value.filter((n) =>
    n.inputs.some((i) => i.id == inputId)
  );

  found.forEach((n) => {
    var inputs = n.inputs.filter((i) => i.id === inputId);
    //delete child nodes from inputs
    inputs.forEach((i) => {
      deleteChild(i.target);
    });
    //delete input
    n.inputs = n.inputs.filter((input) => input.id !== inputId);
  });
  
  //putProjectDataToFlask();
};
const deleteChild = (id) => {
  projectdata.value.forEach((item) => {
    //reset parent input
    item.inputs.forEach((input) => {
      if (input.target === id) input.target = -1;
    });
    //delete connected children
    if (item.id === id) {
      item.inputs.forEach((input) => {
        deleteChild(input.target);
      });
    }
    //
  });

  //delete child
  projectdata.value = projectdata.value.filter((item) => item.id !== id);
  //putProjectDataToFlask();
};
const getInputsById = (id, projectdata) => {
  let obj = projectdata.filter((n) => n.id === id)[0];
  if (obj) return obj.inputs;
};

const getNodeById = (id, projectdata) => {
  //console.log(id)
  let obj = projectdata.filter((n) => n.id === id)[0];
  return obj;
};

const functionListKey = ref(0);

const forceFunctionListRerender = () => {
  functionListKey.value += 1;
};

const inputDialog = (msg) => {
  return prompt(msg, "");
};

provide("addChild", addChild);
provide("addInput", addInput);
provide("deleteChild", deleteChild);
provide("deleteInput", deleteInput);
provide("getInputsById", getInputsById);
provide("getNodeById", getNodeById);
provide("disconnectNodeFromInput", disconnectNodeFromInput);
provide("addNewVarIfNotExisting", addNewVarIfNotExisting);
provide("connectNodeToInput", connectNodeToInput);
provide("checkIfVariableExists", checkIfVariableExists);
provide("putProjectDataToFlask", putProjectDataToFlask);
</script>
<script>
export default {
  components: {
    Function: Function,
	VarInput: VarInput
  },
  props: {
  },
  setup() {
    return {};
  },
  data() {
    return {
      selected: undefined,
	  compileWarnings: []
    };
  },
  methods: {
    showAlert: (msg) => {
      alert(msg);
    },
	delay: (func, time) => {setTimeout(func, time);},
  isVarNameTypeValid (rules, name, acceptableTypes){
      var result = false;
      acceptableTypes.forEach((t) => {
        if (name.match(rules.filter((tv) => tv.type === t)[0].valid)) {
          result = true;
        }
      });
      return result;
    },
  isProgramDataReadyToCompile(data, types) {
	var emptyMem = "???";
	var res = data.some((n) => (n.dyn_inputs && n.inputs.length === 0)) ||
		data.some((n) => (n.mem_loc && n.mem_loc === emptyMem)) ||
		data.some((n) => n.mem_input && !this.isVarNameTypeValid(types, n.mem_loc, n.mem_input)) ||
		data.some((n) => (n.inputs.some((i) => i.target === -1)));

	return !res;
}
  },
  name: "App",

};
</script>

<style></style>
