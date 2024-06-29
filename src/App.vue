<template>
  <!--{{programdata.some((n) => n) === true}}
  <div v-if="programdata.some((n) => n) === true">
    <Function :id="programdata[0].id" :parentId="programdata[0].parentId" :nodes="nodes" :node="nodes[0]"/>
  </div>
  <div v-else>

   </div>-->

  <div v-for="(node, networkId) in programdata.filter((n) => !n.parent)">
    <table>
      <tr>
        <td align="left">Network: {{ networkId + 1 }}</td>
        <td></td>
        <td></td>
      </tr>
      <tr>
        <td>
          <Function
            :id="node.id"
            :networkId="networkId + 1"
            :nodes="programdata"
            :node="programdata.filter((n) => n.id === node.id)[0]"
            :variables="variablesdata"
          />
        </td>
        <td width="20px" valign="top">
            <hr />
        </td>
        <td valign="top">
          <select
            v-model="selected"
            @change="
              connectNodeToInput(node.id, parseInt($event.target.value));
              selected = 'undefined';
            "
          >
            <option disabled="disabled" value="undefined" selected="true">
              ...
            </option>
            <template v-for="n in programdata">
              <template
                v-for="(input, inputNum) in n.inputs"
                v-if="n.networkId !== networkId + 1"
              >
                <option
                  :value="input.id"
                  v-if="
                    input.target === -1 &&
                    (n.dyn_inputs_type === node.output_type ||
                      input.type === node.output_type)
                  "
                >
                  [{{ n.networkId }}]{{ n.block
                  }}{{ input.name === "" ? ":" + inputNum : ":" + input.name }}
                </option>
              </template>

              <!-- <optgroup :label="node.block" >
               <template v-for="block in filterBlocksByOutputType(definition,outputType)">
                <option :value="JSON.stringify(block)">{{ block.name }}</option>
              </template> 
            </optgroup> -->
            </template>
          </select>
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
      outputType="any"
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
        <td>{{variable.name}}</td>
        <td>{{variable.type}}</td>
        <td>                    
            <div v-if="variable.edit === false" style="background-color: transparent" @click="
                variable.edit = true;
                this.$nextTick(() => {
                  this.$refs['desc_input'][0].focus();
                  this.$refs['desc_input'][0].select();
                });
              ">{{variable.description}}&nbsp</div>
            <input ref="desc_input" v-if="variable.edit === true" :value="variable.description" @input="(event) => {variable.description = event.target.value;}" v-on:blur="variable.edit = false">
          </td>
        <td><div v-set="var_refs = programdata.filter((n) => n.mem_id === variable.id).length"></div>{{var_refs}}</td>
        <td align="center"><button class="button button-red" @click="deleteVariable(variable.id)">x</button></td>
      </tr>
    </template>

  </table>

  <br />

  <table>
    <tr>
      <td>
        <textarea cols="30" rows="20">{{ programdata }}</textarea>
    </td>
    <td>
      <textarea cols="30" rows="20">{{ listing }}</textarea>
      <button @click="listing.splice(0);buildListing(programdata)">Compile</button>
    </td>
    <td>
  <textarea cols="30" rows="20">{{ variablesdata }}</textarea>
    </td>
    </tr>
    </table>


</template>

<script setup>
import nodesData from "./assets/program.json";
import varData from "./assets/variables.json";
import definitions from "./assets/definitions.json";
import Function from "./components/Function.vue";
import FunctionList from "./components/FunctionList.vue";
import FunctionListing from "./components/FunctionListing.vue";
import { ref, provide, nextTick } from "vue";
const programdata = ref(nodesData);
const variablesdata = ref(varData);
const listing = ref([])

const recursiveLoopBasedOnInputs = (data, element, parentElement, parentInput) => {
  if(element){
    if(element.input_only === true){
      if(element.parent !== null){
        if(parentElement.dyn_inputs === true)
          listing.value.push(/*parentElement.block + " " + */element.mem_loc);
        else
          listing.value.push(/*parentInput.name + " " + */element.mem_loc);
      }
    }
    else {
      Array.prototype.forEach.call(element.inputs, 
        (input) => {
            if(input.name === "") listing.value.push(element.block);
            else listing.value.push(input.name);

            var nestedElement = data.filter((e) => e.id === input.target)[0];
            if(nestedElement){
              if(nestedElement.input_only !== true)
                listing.value.push("(");
              recursiveLoopBasedOnInputs(data, nestedElement, element, input);
              if(nestedElement.input_only !== true)
                listing.value.push(")");
            }
          });
    }
  }
}

const buildListing = (data, level) => {
  data.forEach(element => {
    if(element.parent === null){
        recursiveLoopBasedOnInputs(data, element, null);
    }
  });
};

const addNewVarIfNotExisting = (name, type) => {
  var found = variablesdata.value.filter((v) => v.name === name)[0];
  if(!found){
    var newVar = {
      id: Date.now(),
      name: name,
      type: type,
      description: "",
      edit: false
    };
    variablesdata.value.push(newVar);
    return newVar.id;
  }
  return found.id;
}

const deleteVariable = (id) => {
  variablesdata.value = variablesdata.value.filter((v) => v.id != id);
  programdata.value.forEach(node => {
    if(node.mem_id === id)
    {
      node.mem_id = 0;
      node.mem_loc = "???";
    }
  });
}

const addChild = (id, parent, blockJson) => {
  var parentId = null;
  var block = JSON.parse(blockJson);
  var inputs = [];
  var inputCounter = 0;
  if (parent) {
    parentId = parent.id;
    parent.target = id;
  }

  programdata.value.push({
    parent: parentId,
    id: id,
    inputs: inputs,
    block: block.name,
    description: "",
    mem_edit: false,
    mem_loc: "???",
    mem_id: 0,
    mem_valid: block.mem_valid,
    mem_required: block.mem_required,
    dyn_inputs: block.dyn_inputs,
    output_type: block.output_type,
    dyn_inputs_type: block.dyn_inputs_type,
    input_only : block.input_only,
    networkId: -1,
    alone: block.alone,
    header_hover: false
  });

  definitions.forEach((group) => {
    group.blocks.forEach((def) => {
      if (def.name === block.name && !def.dyn_inputs && def.inputs) {
        def.inputs.forEach((input) => {
          addInput(id, JSON.stringify(input), inputCounter);
          inputCounter++;
        });
      }
    });
  });
};
const addInput = (nodeId, input, idOffset = 0) => {
  var inputJson = JSON.parse(input ? input : '{"name":"", "type":"none"}');
  let found = programdata.value.filter((item) => item.id === nodeId);

  found.forEach((element) => {
    element.inputs.push({
      id: Date.now() + idOffset,
      target: -1,
      name: inputJson.name,
      type: inputJson.type,
      inverted: false,
      conn_mouse_hover: false,
      input_mouse_hover: false
    });
  });
};

const connectNodeToInput = (nodeId, inputId) => {
  //alert(nodeId + ", " + inputId);
  programdata.value.forEach((node) => {
    if (node.id === nodeId) node.parent = inputId;
    if (node.inputs) {
      node.inputs.forEach((input) => {
        if (input.id === inputId) {
          input.target = nodeId;
          input.type = node.output_type;
          //alert("input.id=" + input.id + "?=" + inputId);
        }
      });
    }
  });
};

const disconnectNodeFromInput = (nodeId, inputId) => {
  //alert(nodeId + ", " + inputId);
  var isInputOnly = false;
  programdata.value.forEach((node) => {
    if (node.id === nodeId) {
      node.parent = null;
      if(node.input_only === true)
        deleteChild(node.id)
    }
    if (node.inputs) {
      node.inputs.forEach((input) => {
        if (input.id === inputId) {
          input.target = -1;
        }
      });
    }
  });

};

const clearInput = (inputId) => {};

const deleteInput = (inputId) => {
  var found = programdata.value.filter((n) =>
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
};
const deleteChild = (id) => {
  programdata.value.forEach((item) => {
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
  programdata.value = programdata.value.filter((item) => item.id !== id);
};
const getInputsById = (id) => {
  let obj = programdata.value.filter((n) => n.id === id)[0];
  if (obj) return obj.inputs;
};

const functionListKey = ref(0);

const forceFunctionListRerender = () => {
  functionListKey.value += 1;
};

provide("addChild", addChild);
provide("addInput", addInput);
provide("deleteChild", deleteChild);
provide("deleteInput", deleteInput);
provide("getInputsById", getInputsById);
provide("disconnectNodeFromInput", disconnectNodeFromInput);
provide("addNewVarIfNotExisting", addNewVarIfNotExisting);

</script>
<script>
export default {
  components: {
    Function: Function,
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
      nodes: nodesData,
      selected: undefined,
    };
  },
};
</script>

<style>

</style>
