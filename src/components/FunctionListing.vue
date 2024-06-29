<template>

<template v-set="(inputsById = getInputsById(id))"></template>
    <template v-for="(input, index) in inputsById">
        <template v-if="nodes.some((n) => n.parent === input.id)">
          <template v-if="input.name === ''">{{node.block}}</template>
          <template v-else>{{input.name}}</template>(
          <FunctionListing
            :id="input.target"
            :networkId="networkId"
            :parentId="input.id"
            :nodes="nodes"
            :node="nodes.filter((n) => n.id === input.target)[0]"
          />)
        </template>
    </template>

</template>
<script setup>
import definitions from "../assets/definitions.json";
import { reactive, computed, nextTick } from "vue";
import { inject } from "vue";

const getInputsById = inject("getInputsById");

</script>
<script>
export default {

  props: ["id", "networkId", "parentId", "nodes", "node"],
  setup() {
    return {};
  },
  methods: {
  },
  computed: {},
  name: "FunctionListing",
  data() {
    return {
    };
  },
};
</script>
<style lang="sccs" scoped></style>
