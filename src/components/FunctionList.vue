<template>

  <select
    @change="$emit('selected', $event.target.value);"
  >
  <option disabled="disabled" selected="selected">...</option>
    <template v-for="definition in definitions">
      <template v-if="checkIfAnyBlockHasType(definition, outputType, alone)">
      <optgroup :label="definition.group" >
        <template v-for="block in filterBlocksByOutputType(definition,outputType,alone)">
          <option :value="JSON.stringify(block)">{{ block.name }}</option>
        </template>
      </optgroup>
      </template>
    </template>
  </select>
</template>
<script setup>
import definitions from "../assets/definitions.json";
</script>
<script>
export default {
  props: ["outputType", "alone"],
  setup() {
    return {};
  },
  methods: {
    checkIfAnyBlockHasType(group, outputType, alone){
      if(alone === true){
        return group.blocks.some((b) => (b.output_type === outputType || outputType === "any") && b.alone === true);
      }
      else{
        return group.blocks.some((b) => b.output_type === outputType || outputType === "any") ;
      }
    },
    filterBlocksByOutputType(group, outputType, alone){
      if(alone === true){
        return group.blocks.filter((b) => (b.output_type === outputType || outputType === "any") && b.alone === true);
      }else{
        return group.blocks.filter((b) => (b.output_type === outputType || outputType === "any"));
      }
    }
  },
  name: "FunctionList",
  data() {
    return {};
  },
};
</script>
<style lang="sccs" scoped></style>
