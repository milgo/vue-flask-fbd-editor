<template>

     <input 
	 ref='focusMe' 
	 type='text' 
	 :value="value" 
	 
	 style="width: 90%; height: 100%"

	 @focus="$event.target.select()" 
	 @blur="$emit('blur')" 
	 @keyup.enter="$emit('enter')"
	 @input="$emit('valueChanged', $event.target.value)"/>

</template>

<script>

export default {
  name: 'VarInput',
  props: ['value'],
  emits: ['valueChanged', 'enter', 'blur'],
  mounted () {

    setTimeout(() => {
       this.$refs.focusMe.focus();
    }, 500);

  }
}

</script>