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
                  @click="deleteChild(id)"
                  v-if="node.header_hover === true"
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
              (isMemValid = isValid(typeDef, node.mem_loc, node.mem_input))
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
              node.mem_edit = true;
              subRefInVariable(node.mem_loc);
              this.$nextTick(() => {
                this.$refs.mem_input.focus();
                this.$refs.mem_input.select();
              });
            "
          >
            {{ node.mem_loc }}<template v-if="node.input_only">&nbsp</template>
            <div
              v-set="
                (varDesc = getVariableDescriptionIfVariableExists(
                  variables,
                  node.mem_id
                ))
              "
            ></div>
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
            <table>
              <tr>
                <td>
                  <input
                    ref="mem_input"
                    style="width: 90%; height: 100%"
                    :value="node.mem_loc"
                    @input="
                      (event) => {
                        node.mem_loc = event.target.value;
                      }
                    "
                    @oro-uwaga="showAlert('teraz')"
                    @blur="memoryEdit(node)"
                    @keyup.enter="memoryEdit(node)"
                  />
                </td>
                <td></td>
              </tr>
            </table>
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
            :node="projectdata.filter((n) => n.id === inputNode.target)[0]"
            :variables="variables"
            :interConnection="interConnection"
            :interConnectionDetails="interConnectionDetails"
            @new-variable="
              (event) =>
                addNewVarIfNotExisting(
                  event.node,
                  event.node.mem_loc,
                  event.node.output_type
                )
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
              class="button button-red"
              @click="
                connectNodeToInput(interConnectionDetails.nodeId, inputNode.id)
              "
            >
              ]
            </button>
          </template>
          <template v-else>
            <template v-if="hasDynInputs(node)">
              <FunctionList
                :outputType="node.dyn_inputs_type"
                :alone="false"
                @selected="addChild(Date.now(), inputNode, $event)"
              />
            </template>
            <template v-else>
              <FunctionList
                :outputType="node.inputs[index].type"
                :alone="false"
                @selected="addChild(Date.now(), inputNode, $event)"
              />
            </template>
          </template>
        </template>
      </td>
      <td align="center" valign="top" width="20px">
        <table
          width="100%"
          @mouseover="inputNode.conn_mouse_hover = true"
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
                    disconnectNodeFromInput(inputNode.target, inputNode.id);
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
                      deleteInput(inputNode.id);
                      deleteChild(inputNode.target);
                    "
                    v-if="inputNode.target === -1"
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
                <template v-if="index === inputsById.length - 1">
                  <button
                    @click="
                      addInput(id, {
                        name: '',
                        type: node.dyn_inputs_type,
                        show_name: 'false',
                      })
                    "
                    class="button button-green"
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
        <template v-if="inputsById.length === 0 && hasDynInputs(node)">
          <button
            @click="
              addInput(id, {
                name: '',
                type: node.dyn_inputs_type,
                show_name: 'false',
              })
            "
            class="button button-green"
          >
            +
          </button>
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
import typeDef from "../assets/type-defs.json";
import { reactive, computed, nextTick } from "vue";
import FunctionList from "./FunctionList.vue";
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
const getMemValidationRules = inject("getMemValidationRules");
const subRefInVariable = inject("subRefInVariable");
const checkIfVariableExists = inject("checkIfVariableExists");
</script>
<script>
export default {
  components: {
    FunctionList: FunctionList,
  },
  props: [
    "id",
    "networkId",
    "parentId",
    "projectdata",
    "node",
    "variables",
    "interConnection",
    "interConnectionDetails",
  ],
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
    getVariableDescriptionIfVariableExists(variables, id) {
      var vars = variables.filter((v) => v.id === id);
      if (vars && vars[0]) return vars[0].description;
      else return "";
    },
    isValid(rules, v, types) {
      var result = false;
      types.forEach((t) => {
        if (v.match(rules.filter((tv) => tv.type === t)[0].valid)) {
          result = true;
        }
      });
      return result;
    },
    isInterconnectionTypeValid() {
      return false;
    },
    memoryEdit(node) {
      //TUTAJ
      node.mem_edit = false;
      if (node.mem_loc === "") {
        node.mem_loc = "???";
        node.mem_id = 0;
      } else {
        if (this.isValid(typeDef, node.mem_loc, node.mem_input)) {
          this.$emit("new-variable", {
            node: node,
            mem_loc: node.mem_loc,
            output_type: node.output_type,
          });
        } else {
          node.mem_id = 0;
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
