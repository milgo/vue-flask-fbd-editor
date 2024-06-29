<template>
  <div v-set="(node.networkId = networkId)"></div>

  <table width=100%>
    <tr>
      <td></td>
      <td></td>
      <td class="fbd-header" width="100px">
        <template v-if="node.input_only === false">
          <table width="100%" >
            <tr>
              <td width="33%" class="fbd-header"></td>
              <td width="34%" class="fbd-header" align="center">    
                <b class="fbd-header">          
                  {{ node.block
                    }}</b>
              </td>
              <td class="fbd-header" width="33%" align="right" valign="top" @mouseover="node.header_hover = true" @mouseleave=" node.header_hover = false">
                <button @click="deleteChild(id)" v-if="node.header_hover === true" class="button button-red">x</button>
              </td>
            </tr>
          </table>
        </template>
      </td>
    </tr>
    <tr>
      <td></td>
      <td></td>
      <td :align="node.input_only?'right':'center'">
        <div v-if="node.mem_required === true">          
            <div
              :class="node.input_only?'fbd-empty '+(node.mem_loc.match(node.mem_valid)?'mem-valid':'mem-invalid') :'fbd-body '+(node.mem_loc.match(node.mem_valid)?'mem-valid':'mem-invalid')"
              v-if="node.mem_edit === false"
              @click="
                node.mem_edit = true;
                this.$nextTick(() => {
                  this.$refs.mem_input.focus();
                  this.$refs.mem_input.select();
                });
              ">
              {{ node.mem_loc }}<template v-if="node.input_only">&nbsp</template>
              <div v-set="varDesc = getVariableDescriptionIfVariableExists(variables, node.mem_id)"></div>
              <b><span class="var-desc" v-if="varDesc!=''">"{{varDesc}}"</span></b>
            </div>
            <div v-else>
              <table>
                <tr>
                  <td>
                    <input
                      ref="mem_input"
                      style="width: 90%; height: 100%"
                      :value="node.mem_loc"
                      @input="(event) => {node.mem_loc = event.target.value;}"
                      v-on:blur="{
                        node.mem_edit = false;
                        if(node.mem_loc==='')
                        {
                          node.mem_loc='???';
                          node.mem_id=0;
                        }else{
                          if(node.mem_loc.match(node.mem_valid)){
                            node.mem_id = addNewVarIfNotExisting(node.mem_loc, node.output_type);
                          }
                          else{
                            node.mem_id = 0;
                          }
                        }
                        }"
                    />
                  </td>
                  <td></td>
                </tr>
              </table>
            </div>
          
        </div>
      </td>
    </tr>
<div v-set="(inputsById = getInputsById(id))"></div>
    <tr v-for="(input, index) in inputsById">
      <td align="right" valign="top">
        <template v-if="nodes.some((n) => n.parent === input.id)">
          <Function
            :id="input.target"
            :networkId="networkId"
            :parentId="input.id"
            :nodes="nodes"
            :node="nodes.filter((n) => n.id === input.target)[0]"
            :variables="variables"
          />
        </template>
        <template v-else>
          <template v-if="hasDynInputs(node)">
            <FunctionList
              :outputType="node.dyn_inputs_type"
              :alone="false"
              @selected="addChild(Date.now(), input, $event)"
            />
          </template>
          <template v-else>
            <FunctionList
              :outputType="input.type"
              :alone="false"
              @selected="addChild(Date.now(), input, $event)"
            />
          </template>
        </template>
      </td>
      <td
        align="center"
        valign="top"
        width="20px"
         
      >

         <table width="100%" @mouseover="input.conn_mouse_hover = true" @mouseleave="input.conn_mouse_hover = false">
            <tr>
              <td>
                <div v-if="input.conn_mouse_hover === false || input.target === -1"><hr /></div>
              </td>
              <td>
                <div v-if="input.target !== -1 && input.conn_mouse_hover === true">
                  <button @click="disconnectNodeFromInput(input.target, input.id); input.conn_mouse_hover = false;" class="button button-red">x</button>
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
            : 'fbd-body'
        "
        align="left"
        valign="top" 
      >
        <template v-if="hasDynInputs(node)">
          <table width="100%">
            <tr>
              <td class="fbd-body"  @mouseover="input.input_mouse_hover = true" @mouseleave="input.input_mouse_hover = false">
                <template v-if="input.input_mouse_hover === true">
                <button
                  @click="
                    deleteInput(input.id);
                    deleteChild(input.target);
                  "
                  v-if="input.target === -1"
                  class="button button-red"
                >x</button>
                </template>
                <template else></template>
                <template v-if="index !== inputsById.length - 1"><br /></template>
                <template v-else></template>
                <br />
              </td>
            </tr>
            <tr>
              <td class="fbd-body">
                <template v-if="index === inputsById.length - 1">
                  <button @click="addInput(id)" class="button button-green">+</button>
                </template>
              </td>
            </tr>
          </table>
        </template>
        <template v-else>
          <table width="100%">
            <tr>
              <td class="fbd-body">
                &nbsp<small
                  ><b class="fbd-body fbd-header">{{ input.name }}</b></small
                ><br />&nbsp
              </td>
            </tr>
          </table>
        </template>
      </td>
    </tr>
    <tr>
      <td></td>
      <td ></td>
      <td class="fbd-body" align="left">
        <template v-if="inputsById.length === 0 && hasDynInputs(node)">
          <button @click="addInput(id)" class="button button-green">+</button>
        </template>
      </td>
    </tr>
    <tr>
      <td>&nbsp</td>
      <td ></td>
      <td></td>
    </tr>
  </table>

</template>
<script setup>
import definitions from "../assets/definitions.json";
import { reactive, computed, nextTick } from "vue";
import FunctionList from "./FunctionList.vue";
//import vClickOutside from 'click-outside-vue3';
import { inject } from "vue";

//const contextMenu = require('vue-dynamic-context-menu');
const addChild = inject("addChild");
const deleteChild = inject("deleteChild");
const addInput = inject("addInput");
const getInputsById = inject("getInputsById");
const deleteInput = inject("deleteInput");
const disconnectNodeFromInput = inject("disconnectNodeFromInput");
const addNewVarIfNotExisting = inject("addNewVarIfNotExisting");

</script>
<script>
export default {
  components: {
    FunctionList: FunctionList
  },
  props: ["id", "networkId", "parentId", "nodes", "node", "variables"],
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
    getVariableDescriptionIfVariableExists(variables, id){
      var vars = variables.filter((v) => v.id === id);
      if(vars && vars[0])
        return vars[0].description;
      else return "";
    }
  },
  computed: {},
  name: "Function",
  data() {
    return {
    };
  },
};
</script>
<style lang="sccs" scoped></style>
