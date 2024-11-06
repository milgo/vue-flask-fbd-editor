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
            :node="projectdata.filter((n) => n.id === node.id)[0]"
            :variables="variablesdata"
            :interConnection="interConnection"
            :interConnectionDetails="interConnectionDetails"
          />
        </td>
        <td width="20px" valign="top">
          <hr />
        </td>
        <td valign="top">
          <button
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

  <div align="left">
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
      <th>Action</th>
    </tr>

    <template v-for="variable in variablesdata">
      <tr>
        <td>
          <div
            v-if="variable.edit === false || variable.refs > 0"
            @click="
              variable.edit = variable.refs === 0;
              if (variable.refs === 0) {
                this.$nextTick(() => {
                  this.$refs['mem_input'][0].focus();
                  this.$refs['mem_input'][0].select();
                });
              }
            "
            style="background-color: transparent"
          >
            {{ variable.name }}
          </div>
          <input
            ref="mem_input"
            v-if="variable.edit === true && variable.refs === 0"
            :value="variable.name"
            @input="
              (event) => {
                variable.name = event.target.value;
              }
            "
            v-on:blur="variable.edit = false"
            @keyup.enter="
              {
                variable.edit = false;
                if (variable.name === '') {
                  variable.name = '???';
                } else {
                  if (checkIfVariableExists(variable.name)) {
                    showAlert('Variable ' + variable.name + ' already exists.');
                    variable.name = '???';
                  }
                }
              }
            "
          />
        </td>
        <td>{{ variable.type }}</td>
        <td>
          <div
            v-if="variable.edit === false"
            style="background-color: transparent"
            @click="
              variable.edit = true;
              this.$nextTick(() => {
                this.$refs['desc_input'][0].focus();
                this.$refs['desc_input'][0].select();
              });
            "
          >
            {{ variable.description }}&nbsp
          </div>
          <input
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
          />
        </td>
        <td>
          {{
            projectdata.filter(
              (n) =>
                n.mem_loc === variable.name && n.mem_input === variable.type
            ).length
          }}
        </td>
        <td align="center">
          <button
            class="button button-red"
            @click="deleteVariable(variable.id)"
          >
            x
          </button>
        </td>
      </tr>
    </template>
  </table>

  <div v-set="(varName = '???')"></div>
  <select
    v-model="selected"
    @change="
      varName = inputDialog('Enter variable name: ');
      if (
        varName.match(
          memDefs.filter((md) => md.type === $event.target.value)[0].valid
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
    <template v-for="m in memDefs">
      <option :value="m.type">{{ m.type }}</option>
    </template>
  </select>

  <br />

  <table>
    <tr>
      <td>
        <textarea cols="30" rows="20">{{ projectdata }}</textarea>
      </td>
      <td>
        <textarea cols="30" rows="20">{{ listing }}</textarea>
        <button
          @click="
            listing.splice(0);
            buildListing(projectdata);
			putCompileDataToFlask();
          "
        >
          Compile
        </button>
		<button
          @click="
            axios.get('http://localhost:5000/start')
          "
        >
          Start
        </button>
      </td>
      <td>
        <textarea cols="30" rows="20">{{ variablesdata }}</textarea>
      </td>
    </tr>
  </table>
  {{ interConnectionDetails }}
</template>

<script setup>
import axios from "axios";
import varData from "./assets/variables.json";
import definitions from "./assets/definitions.json";
import memDefinitions from "./assets/type-defs.json";
import Function from "./components/Function.vue";
import FunctionList from "./components/FunctionList.vue";
import FunctionListing from "./components/FunctionListing.vue";
import { ref, provide, nextTick, onMounted } from "vue";
const projectdata = ref([]);
const listing = ref([]);
const variablesdata = ref(varData);
const memDefs = ref(memDefinitions);
const interConnection = ref(false);
const interConnectionDetails = ref({
  nodeId: 0,
  networkId: -1,
  outputType: ["any"],
});

function diselectInterConnection() {
  interConnection.value = false;
}

const recursiveLoopBasedOnInputs = (
  data,
  element,
  parentElement,
  parentInput
) => {
  if (element) {
    if (element.input_only === true) {
      listing.value.push({
        function:
          parentElement.alias != "" ? parentElement.alias : parentElement.block,
        memory: element.mem_loc,
        node: element.id,
        target: parentElement.id,
      });
    } else {
      listing.value.push({
        function:
          "pre_" + (element.alias != "" ? element.alias : element.block),
        target: element.id,
      });

      Array.prototype.forEach.call(element.inputs, (input) => {
        var nestedElement = data.filter((e) => e.id === input.target)[0];
        recursiveLoopBasedOnInputs(data, nestedElement, element, input);
      });

      listing.value.push({
        function:
          "post_" + (element.alias != "" ? element.alias : element.block),
        memory: element.mem_loc !== "???" ? element.mem_loc : undefined,
        target: element.id,
      });
    }
  }
};

const buildListing = (data, level) => {
  data.forEach((element) => {
    if (element.parentInput === null) {
      listing.value.push({ function: "CANCEL_RLO" });
      recursiveLoopBasedOnInputs(data, element, null);
    }
  });
};

const checkIfVariableExists = (name) => {
  return variablesdata.value.filter((v) => v.name === name)[0];
};

const addNewVarIfNotExisting = (node, name, type) => {
  var found = checkIfVariableExists(name);
  if (!found) {
    var newVar = {
      id: Date.now(),
      name: name,
      type: type,
      description: "",
      edit: false,
    };
    variablesdata.value.push(newVar);
    return newVar.id;
  }
  return found.id;
};

const deleteVariable = (id) => {
  var varName = variablesdata.value.filter((v) => v.id === id)[0].name;
  variablesdata.value = variablesdata.value.filter((v) => v.id != id);
  projectdata.value.forEach((node) => {
    if (node.mem_loc === varName) {
      node.mem_loc = "???";
    }
  });
};

const getProgramDataFromFlask = () => {
  const path = "http://localhost:5000/project";//"/program";
	axios.get(path).then((res) => {console.log(res.data);projectdata.value = res.data.projectdata;})
		.catch((err) => console.error(err));
}

const putProgramDataToFlask = () => {
  const path = "http://localhost:5000/project";//"/program";
  axios.post(path, projectdata.value)
        .then(() => {
          axios.get(path).then((res) => {projectdata.value = res.data.projectdata;})
            .catch((err) => console.error(err));
        }).catch((err) => console.error(err));
}

const putCompileDataToFlask = () => {
  const path = "http://localhost:5000/compile";//"/program";
  axios.post(path, listing.value).catch((err) => console.error(err));
}


onMounted(() => {
  getProgramDataFromFlask();
})

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
    mem_loc: "???",
    //mem_id: 0,
    mem_input: block.mem_input,
    dyn_inputs: block.dyn_inputs,
    output_type: block.output_type,
    dyn_inputs_type: block.dyn_inputs_type,
    input_only: block.input_only,
    networkId: -1,
    header_hover: false,
    value: 0,
  });

  definitions.forEach((group) => {
    group.blocks.forEach((def) => {
      if (def.name === block.name && !def.dyn_inputs && def.inputs) {
        def.inputs.forEach((inputDef) => {
          addInput(id, inputDef, inputCounter);
          inputCounter++;
        });
      }
    });
  });
  putProgramDataToFlask();
};
const addInput = (nodeId, inputDef, idOffset = 0) => {
  // var inputJson = JSON.parse(input /*? input : '{"name":"", "type":"none"}'*/);
  let found = projectdata.value.filter((item) => item.id === nodeId);

  found.forEach((element) => {
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
  putProgramDataToFlask();
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
  putProgramDataToFlask();
};

const disconnectNodeFromInput = (nodeId, inputId) => {
  //alert(nodeId + ", " + inputId);
  var isInputOnly = false;
  projectdata.value.forEach((node) => {
    if (node.id === nodeId) {
      node.parentInput = null;
      if (node.input_only === true) {
        subRefInVariable(node.mem_loc);
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
  putProgramDataToFlask();
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
  
  putProgramDataToFlask();
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
  putProgramDataToFlask();
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

const getMemValidationRules = (memType) => {
  var res = memDefs.value.filter((d) => d.type === memType);
  if (res && res[0]) return res[0].valid;
  return "";
};

const subRefInVariable = (name) => {
  var res = variablesdata.value.filter((v) => v.name === name);
  if (res && res[0] && res[0].refs > 0) res[0].refs--;
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
provide("getMemValidationRules", getMemValidationRules);
provide("subRefInVariable", subRefInVariable);
provide("checkIfVariableExists", checkIfVariableExists);
</script>
<script>
export default {
  components: {
    Function: Function,
  },
  props: {
    projectdata: {
      type: Array,
      default: () => [],
    },
  },
  setup() {
    return {};
  },
  methods: {
    showAlert: (msg) => {
      alert(msg);
    },
  },
  name: "App",
  data() {
    return {
      selected: undefined,
    };
  },
};
</script>

<style></style>
