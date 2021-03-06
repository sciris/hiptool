<!--
PopupSpinner component

Based on MoonLoader.vue from vue-spinner GitHub project:
https://github.com/greyby/vue-spinner/blob/master/src/MoonLoader.vue 

Depends also on vue-js-modal GitHub project:
https://github.com/euvl/vue-js-modal

Last update: 2018-08-13
-->

<template>
  <modal name="popup-spinner"
         :height="modalHeight"
         :width="modalWidth"
         style="opacity: 1.0" 
         :click-to-close="false" 
         @before-open="beforeOpen" 
         @before-close="beforeClose">
         
    <div :style="spinnerWrapStyle">
      <div class="v-spinner" v-show="loading">
        <div class="v-moon v-moon1" :style="spinnerStyle">
          <div class="v-moon v-moon2" :style="[spinnerMoonStyle,animationStyle2]">
          </div>
          <div class="v-moon v-moon3" :style="[spinnerStyle,animationStyle3]">
          </div>
        </div>
      </div>
    </div>
    
    <div v-if="title !== ''" :style="titleStyle">
      {{ title }}
    </div>
    
    <div v-if="hasCancelButton" style="padding: 13px">
      <button @click="cancel" :style="cancelButtonStyle">Cancel</button>
    </div>    
  </modal>
</template>

<script>
  import SpinnerPlugin from './index'  // used to access the event bus
  
  export default {
    name: 'PopupSpinner',
    
    props: {
      loading: {
        type: Boolean,
        default: true
      },
     title: {
        type: String,
        default: ''      
      },
      hasCancelButton: {
        type: Boolean,
        default: false      
      }, 
      color: {
        type: String,
        default: '#0000ff'
      },
      size: {
        type: String,
        default: '50px'
      },
      margin: {
        type: String,
        default: '2px'
      },
      padding: {
        type: String,
        default: '15px'      
      },
      radius: {
        type: String,
        default: '100%'
      }
    },
    
    data() {
      return {
        spinnerStyle: {
          height: this.size,
          width: this.size,
          borderRadius: this.radius
        },
        spinnerWrapStyle: {
          padding: this.padding
        }, 
        titleStyle: {
          textAlign: 'center'
        },
        cancelButtonStyle: {
          padding: '2px'
        },          
        opened: false
      }
    },
    
    beforeMount() {
      // Create listener for start event.
      SpinnerPlugin.eventBus.$on('start', () => {
        this.show()
      })
      
      // Create listener for stop event.
      SpinnerPlugin.eventBus.$on('stop', () => {
        this.hide()
      })      
    },
    
    computed: {
      modalHeight() {
        // Start with the height of the spinner wrapper.
        let fullHeight = parseFloat(this.size) + 2 * parseFloat(this.padding)
        
        // If there is a title there, add space for the text.
        if (this.title !== '') {
          fullHeight = fullHeight + 20 + parseFloat(this.padding)        
        }
        
        // If there is a cancel button there, add space for it.
        if (this.hasCancelButton) {
          fullHeight = fullHeight + 20 + parseFloat(this.padding)
        }
        
        return fullHeight + 'px'
      },
      
      modalWidth() {
        return parseFloat(this.size) + 2 * parseFloat(this.padding) + 'px'
      },
      
      moonSize() {
        return parseFloat(this.size)/7
      },
      
      spinnerMoonStyle() {
        return {
          height: this.moonSize  + 'px',
          width: this.moonSize  + 'px',
          borderRadius: this.radius
        }
      },
      
      animationStyle2() {
        return {
          top: parseFloat(this.size)/2 - this.moonSize/2 + 'px',
          backgroundColor: this.color
        }
      },
      
      animationStyle3() {
        return {
          border: this.moonSize + 'px solid ' + this.color
        }
      }
    }, 
    
    methods: {
      beforeOpen() {
        window.addEventListener('keyup', this.onKey)
        this.opened = true
      }, 
      
      beforeClose() {
        window.removeEventListener('keyup', this.onKey)
        this.opened = false
      }, 
      
      onKey(event) {
        if (event.keyCode == 27) {
          console.log('Exited spinner through Esc key')
          this.cancel()
        }
      }, 
      
      cancel() {
        this.$emit('spinner-cancel')
        this.hide()      
      },
      
      show() {
        this.$modal.show('popup-spinner') // Bring up the spinner modal.
      },
      
      hide() {
        this.$modal.hide('popup-spinner') // Dispel the spinner modal.
      }
    }

  }
</script>

<style>

  .v-spinner .v-moon1
  {

    -webkit-animation: v-moonStretchDelay 0.6s 0s infinite linear;
    animation: v-moonStretchDelay 0.6s 0s infinite linear;
    -webkit-animation-fill-mode: forwards;
    animation-fill-mode: forwards;
    position: relative;
  }

  .v-spinner .v-moon2
  {
    -webkit-animation: v-moonStretchDelay 0.6s 0s infinite linear;
    animation: v-moonStretchDelay 0.6s 0s infinite linear;
    -webkit-animation-fill-mode: forwards;
    animation-fill-mode: forwards;
    opacity: 0.9;
    position: absolute;
  }

  .v-spinner .v-moon3
  {
    opacity: 0.1;
  }

  @-webkit-keyframes v-moonStretchDelay
  {
    100%
    {
      -webkit-transform: rotate(360deg);
      transform: rotate(360deg);
    }
  }

  @keyframes v-moonStretchDelay
  {
    100%
    {
      -webkit-transform: rotate(360deg);
      transform: rotate(360deg);
    }
  }

  .vue-dialog div {
    box-sizing: border-box;
  }
  .vue-dialog .dialog-flex {
    width: 100%;
    height: 100%;
  }
  .vue-dialog .dialog-content {
    flex: 1 0 auto;
    width: 100%;
    padding: 15px;
    font-size: 14px;
  }
  .vue-dialog .dialog-c-title {
    font-weight: 600;
    padding-bottom: 15px;
  }
  .vue-dialog .dialog-c-text {
  }
  .vue-dialog .vue-dialog-buttons {
    display: flex;
    flex: 0 1 auto;
    width: 100%;
    border-top: 1px solid #eee;
  }
  .vue-dialog .vue-dialog-buttons-none {
    width: 100%;
    padding-bottom: 15px;
  }
  .vue-dialog-button {
    font-size: 12px !important;
    background: transparent;
    padding: 0;
    margin: 0;
    border: 0;
    cursor: pointer;
    box-sizing: border-box;
    line-height: 40px;
    height: 40px;
    color: inherit;
    font: inherit;
    outline: none;
  }
  .vue-dialog-button:hover {
    background: rgba(0, 0, 0, 0.01);
  }
  .vue-dialog-button:active {
    background: rgba(0, 0, 0, 0.025);
  }
  .vue-dialog-button:not(:first-of-type) {
    border-left: 1px solid #eee;
  }

</style>