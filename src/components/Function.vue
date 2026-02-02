<template>

  <div v-set="(node.networkId = networkId)"></div>
  <table width="100%">
    <tr>
      <td></td>
      <td></td>
      <td :class="node.value ? 'fbd-header-green' : 'fbd-header'" width="100px">
        <template v-if="node.input_only === false">
          <table width="100%">
            <tr>
              <td
                width="33%"
                :class="node.value ? 'fbd-header-green' : 'fbd-header'"
              ></td>
              <td
                width="34%"
                :class="node.value ? 'fbd-header-green' : 'fbd-header'"
                align="center"
              >
                <b :class="node.value ? 'fbd-header-green' : 'fbd-header'">
                  {{ node.block }}
                </b>
              </td>
              <td
                :class="node.value ? 'fbd-header-green' : 'fbd-header'"
                width="33%"
                align="right"
                valign="top"
                @mouseover="node.header_hover = true"
                @mouseleave="node.header_hover = false"
              >
                <button
                  @click="
				    pushProjectAndVariablesToUndoStack();
					deleteChild(id);
					putProjectData()
					"
                  v-if="node.header_hover === true && enableEdit"
                  class="button button-red"
                >
                  x
                </button>
              </td>
            </tr>
          </table>
        </template>
      </td>
    </tr>
    <tr>
      <td></td>
      <td></td>
      <td :align="node.input_only ? 'right' : 'center'">
        <div v-if="node.mem_input">
          <div
            v-set="
              (isMemValid = isVarNameTypeValid(varTypes, node.mem_loc, node.mem_input))
            "
          ></div>
          <div
            :class="
              node.input_only
                ? 'fbd-empty ' + (isMemValid ? 'mem-valid' : 'mem-invalid')
                : (node.value ? 'fbd-body-green' : 'fbd-body') +
                  ' ' +
                  (isMemValid ? 'mem-valid' : 'mem-invalid')
            "
            v-if="node.mem_edit === false"
            @click="
			  pushProjectAndVariablesToUndoStack();
              node.mem_edit = enableEdit;
            "
          >
            {{ node.mem_loc }}<template v-if="node.input_only">&nbsp</template>
			<div class="tooltip" v-if="!isMemValid">
				<img src="../assets/warning.png"/><span class="tooltiptext">Memory not assigned</span>
			</div>
            <div
              v-set="
                (varDesc = getVariableDescriptionIfVariableExists(
                  variables,
                  node.mem_loc
                ))
              "
            ></div>
			<!-- monitor data -->
			<template v-if="isInMonitorMode">
			{{getVariableMonitorDataIfVariableExists(variables, node.mem_loc)}}
			<br/></template>
            <b
              ><span
                :class="
                  node.value
                    ? 'var-desc fbd-body-green'
                    : node.input_only
                    ? 'var-desc'
                    : 'var-desc fbd-body'
                "
                v-if="varDesc != ''"
                >"{{ varDesc }}"</span
              ></b
            >
          </div>
          <div v-else>

				<VarInput 
				@blur="node.mem_edit = false; delayWithParam((n) => {memoryEdit(n);}, 500, node);" 
				@enter="memoryEdit(node)"
				:value="node.mem_loc"
				@valueChanged="(value) => node.mem_loc = value"
				/>

          </div>
        </div>
      </td>
    </tr>
    <div v-set="(inputsById = getInputsById(id, projectdata))"></div>
    <tr v-for="(inputNode, index) in inputsById">
      <td align="right" valign="top">
        <template v-if="projectdata.some((n) => n.parentInput === inputNode.id)">
          <Function
            :id="inputNode.target"
            :networkId="networkId"
            :parentId="inputNode.id"
            :projectdata="projectdata"
			:enableEdit="enableEdit"
			:isInMonitorMode="isInMonitorMode"
            :node="projectdata.filter((n) => n.id === inputNode.target)[0]"
            :variables="variables"
            :interConnection="interConnection"
            :interConnectionDetails="interConnectionDetails"
            @new-variable="
              (event) => {
                addNewVarIfNotExisting(
                  event.node,
                  event.mem_loc,
                  event.output_type
                );
				putProjectData();
				}
            "
          />
        </template>
        <template v-else>
          <template
            v-if="
              interConnection &&
              interConnectionDetails.networkId !== node.networkId &&
              node.inputs[index].type.some(
                (t) => interConnectionDetails.outputType === t
              )
            "
          >
            <button
			  v-if="enableEdit"
              class="button button-red"
              @click="
			    pushProjectAndVariablesToUndoStack();
                connectNodeToInput(interConnectionDetails.nodeId, inputNode.id);
				putProjectData();
              "
            >
              ]
            </button>
          </template>
          <template v-else>

			<div class="tooltip"><img src="../assets/warning.png"/>
			  <span class="tooltiptext">Input not assigned</span>
			</div>

            <template v-if="hasDynInputs(node) && enableEdit">
              <FunctionList
                :outputType="node.dyn_inputs_type"
                :alone="false"
                @selected="pushProjectAndVariablesToUndoStack();addChild(Date.now(), inputNode, $event);putProjectData();"
              />
            </template>
            <template v-else>
              <FunctionList 
				v-if="enableEdit"
                :outputType="node.inputs[index].type"
                :alone="false"
                @selected="pushProjectAndVariablesToUndoStack();addChild(Date.now(), inputNode, $event);putProjectData();"
              />
            </template>
          </template>
        </template>
      </td>
      <td align="center" valign="top" width="20px">
        <table
          width="100%"
          @mouseover="inputNode.conn_mouse_hover = enableEdit"
          @mouseleave="inputNode.conn_mouse_hover = false"
        >
          <tr>
            <td>
              <div v-if="inputNode.conn_mouse_hover === false">
                <hr
                  v-if="inputNode.target !== -1"
                  :class="
                    getNodeById(inputNode.target, projectdata).value === 0
                      ? 'hr-normal'
                      : 'hr-green'
                  "
                />
				<!--<hr
                  v-if="inputNode.target !== -1"
                  :class="
                    inputNode.value === 0
                      ? 'hr-normal'
                      : 'hr-green'
                  "
                />-->
                <hr v-if="inputNode.target === -1" class="hr-normal" />
              </div>
              <div v-else>
                <hr v-if="inputNode.target === -1" class="hr-normal" />
              </div>
            </td>
            <td>
              <div
                v-if="
                  inputNode.target !== -1 && inputNode.conn_mouse_hover === true
                "
              >
                <button				  
                  @click="
				    pushProjectAndVariablesToUndoStack();
                    disconnectNodeFromInput(inputNode.target, inputNode.id);
					putProjectData();
                    inputNode.conn_mouse_hover = false;
                  "
                  class="button button-red"
                >
                  x
                </button>
              </div>
            </td>
            <td></td>
          </tr>
        </table>
      </td>
      <td
        :class="
          index === inputsById.length - 1
            ? 'fbd-empty'
            : node.value
            ? 'fbd-body-green'
            : 'fbd-body'
        "
        align="left"
        valign="top"
      >
        <template v-if="hasDynInputs(node)">
          <table width="100%">
            <tr>
              <td
                :class="node.value ? 'fbd-body-green' : 'fbd-body'"
                @mouseover="inputNode.input_mouse_hover = true"
                @mouseleave="inputNode.input_mouse_hover = false"
              >
                <template v-if="inputNode.input_mouse_hover === true">
                  <button
                    @click="
					  pushProjectAndVariablesToUndoStack();
                      deleteInput(inputNode.id);
                      deleteChild(inputNode.target);
					  putProjectData();
                    "
                    v-if="inputNode.target === -1 && enableEdit"
                    class="button button-red"
                  >
                    x
                  </button>
                </template>
                <template else></template>
                <template v-if="index !== inputsById.length - 1"
                  ><br
                /></template>
                <template v-else></template>
                <br />
              </td>
            </tr>
            <tr>
              <td :class="node.value ? 'fbd-body-green' : 'fbd-body'">
                <template v-if="index === inputsById.length - 1 && enableEdit">
                  <button
                    @click="
					  pushProjectAndVariablesToUndoStack();
                      addInput(id, {
                        name: '',
                        type: node.dyn_inputs_type,
                        show_name: 'false',
                      });
					  putProjectData();
                    "
                    class="button button-orange"
                  >
                    +
                  </button>
                </template>
              </td>
            </tr>
          </table>
        </template>
        <template v-else>
          <table width="100%">
            <tr>
              <td :class="node.value ? 'fbd-body-green' : 'fbd-body'">
                &nbsp<small
                  ><b
                    :class="
                      node.value ? 'fbd-body-green' : 'fbd-body fbd-header'
                    "
                    v-if="inputNode.show_name === true"
                    >{{ inputNode.name }}
                  </b></small
                ><br />&nbsp
              </td>
            </tr>
          </table>
        </template>
      </td>
    </tr>
    <tr>
      <td></td>
      <td></td>
      <td :class="node.value ? 'fbd-body-green' : 'fbd-body'" align="left">
        <template v-if="inputsById.length === 0 && hasDynInputs(node) && enableEdit">

          <button
            @click="
			  pushProjectAndVariablesToUndoStack();
              addInput(id, {
                name: '',
                type: node.dyn_inputs_type,
                show_name: 'false',
              });
			  putProjectData();
            "
            class="button button-orange"
          >
            +
          </button>
		  <div class="tooltip" v-if="!isMemValid">
			<img src="../assets/warning.png"/><span class="tooltiptext">No inputs added</span>
		  </div>
        </template>
      </td>
    </tr>
    <tr>
      <td>&nbsp</td>
      <td></td>
      <td></td>
    </tr>
  </table>
</template>
<script setup>
import definitions from "../assets/definitions.json";
import varTypes from "../assets/var-types.json";
import { reactive, computed } from "vue";
import FunctionList from "./FunctionList.vue";
import VarInput from "./VarInput.vue";
//import vClickOutside from 'click-outside-vue3';
import { inject } from "vue";

//const contextMenu = require('vue-dynamic-context-menu');
const addChild = inject("addChild");
const deleteChild = inject("deleteChild");
const addInput = inject("addInput");
const getInputsById = inject("getInputsById");
const getNodeById = inject("getNodeById");
const deleteInput = inject("deleteInput");
const disconnectNodeFromInput = inject("disconnectNodeFromInput");
const addNewVarIfNotExisting = inject("addNewVarIfNotExisting");
const connectNodeToInput = inject("connectNodeToInput");
const checkIfVariableExists = inject("checkIfVariableExists");
const pushProjectAndVariablesToUndoStack = inject("pushProjectAndVariablesToUndoStack");
const putProjectData = inject("putProjectData");
</script>
<script>
export default {
  components: {
    FunctionList: FunctionList,
	VarInput: VarInput
  },
  props: [
    "id",
    "networkId",
    "parentId",
    "projectdata",
	"enableEdit",
	"isInMonitorMode",
    "node",
    "variables",
    "interConnection",
    "interConnectionDetails",
  ],
  emits: ["new-variable"], 
  setup() {
    return {};
  },
  methods: {
    hasDynInputs(node) {
      return definitions.some((g) =>
        g.blocks.some((b) => b.name === node.block && b.dyn_inputs === true)
      );
    },
    showAlert: (msg) => {
      alert(msg);
    },
    getVariableDescriptionIfVariableExists(variables, mem_loc) {
      var vars = variables.filter((v) => v.name === mem_loc);
      if (vars && vars[0]) return vars[0].description;
      else return "";
    },
	getVariableMonitorDataIfVariableExists(variables, mem_loc) {
      var vars = variables.filter((v) => v.name === mem_loc);
      if (vars && vars[0]) return vars[0].monitorData;
      else return "";
	},
    isVarNameTypeValid (rules, name, acceptableTypes){
      var result = false;
      acceptableTypes.forEach((t) => {
        if (name.match(rules.filter((tv) => tv.type === t)[0].valid)) {
          result = true;
        }
      });
      return result;
    },
    isInterconnectionTypeValid() {
      return false;
    },
	delayWithParam: (func, time, param) => {setTimeout(func, time, param);},
    memoryEdit(node) {
      node.mem_edit = false;
      if (node.mem_loc === "") {
        node.mem_loc = "???";
      } else {
        if (this.isVarNameTypeValid(varTypes, node.mem_loc, node.mem_input)) {
          this.$emit("new-variable", {
            node: node,
            mem_loc: node.mem_loc,
            output_type: varTypes.filter((t) => node.mem_loc.match(t.valid))[0].type//node.output_type,
          });
        }
      }
    },
  },
  computed: {},
  name: "Function",
  data() {
    return {};
  },
};
</script>
<style lang="sccs" scoped></style>
