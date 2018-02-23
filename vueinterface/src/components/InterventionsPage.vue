<!-- 
InterventionsPage.vue -- InterventionsPage Vue component

Last update: 2/23/18 (gchadder3)
-->

<template>
  <div class="SitePage">
    <h2>Open Project: Afghanistan test 1</h2>

    <div class="PageSection">
      <input type="text" 
             class="txbox" 
             style="margin-bottom: 20px" 
             :placeholder="filterPlaceholder"
             v-model="filterText"/>

      <table class="table table-bordered table-hover table-striped" style="width: auto">
        <thead>
          <tr>
            <th @click="updateSorting('name')" class="sortable">
              Intervention set
              <span v-show="sortColumn == 'name' && !sortReverse">
                <i class="fas fa-caret-down"></i>
              </span>
              <span v-show="sortColumn == 'name' && sortReverse">
                <i class="fas fa-caret-up"></i>
              </span>
              <span v-show="sortColumn != 'name'">
                <i class="fas fa-caret-up" style="visibility: hidden"></i>
              </span>
            </th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="intervSet in sortedFilteredIntervSets" :class="{ highlighted: activeIntervSet.uid === intervSet.uid }">
            <td>{{ intervSet.setName }}</td>
            <td style="white-space: nowrap">
              <button class="btn __green" @click="viewSet(intervSet.uid)">View</button>
              <button class="btn" @click="copySet(intervSet.uid)">Copy</button>
              <button class="btn" @click="renameSet(intervSet.uid)">Rename</button>
              <button class="btn __red" @click="deleteSet(intervSet.uid)">Delete</button>
            </td>
          </tr>
          <tr>
            <td>
              <button class="btn" @click="createNewSet">Create new</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <div class="PageSection UIPlaceholder" v-if="activeIntervSet.setName != undefined">
      <div class="PHText">
        Page interface specific to {{ activeIntervSet.setName }} intervention set
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
var filesaver = require('file-saver')
import rpcservice from '../services/rpc-service'
import router from '../router'

export default {
  name: 'InterventionsPage',

  data() {
    return {
      // Placeholder text for table filter box
      filterPlaceholder: '\u{1f50e} Filter Intervention Set',

      // Text in the table filter box
      filterText: '',

      // Column of table used for sorting the intervention sets
      sortColumn: 'name',  // name

      // Sort in reverse order?
      sortReverse: false, 

      // List of objects for intervention sets the project has
      interventionSets: 
        [
          {
            setName: 'Default LMIC from DCP',
            uid: 1
          }, 
          {
            setName: 'Country defined set',
            uid: 2
          }
        ],

      // Active intervention set
      activeIntervSet: {},
    }
  },

  computed: {
    sortedFilteredIntervSets() {
      return this.applyNameFilter(this.applySorting(this.interventionSets))
    } 
  }, 

  created() {
    // If we have no user logged in, automatically redirect to the login page.
    if (this.$store.state.currentuser.displayname == undefined) {
      router.push('/login')
    }
  },

  methods: {
    updateSorting(sortColumn) {
      console.log('updateSorting() called')

      // If the active sorting column is clicked...
      if (this.sortColumn === sortColumn) {
          // Reverse the sort.
          this.sortReverse = !this.sortReverse
      } 
      // Otherwise.
      else {
        // Select the new column for sorting.
        this.sortColumn = sortColumn

        // Set the sorting for non-reverse.
        this.sortReverse = false
      }
    },

    applyNameFilter(sets) {
      console.log('applyNameFilter() called')

      return sets.filter(theSet => theSet.setName.toLowerCase().indexOf(this.filterText.toLowerCase()) !== -1)
    },

    applySorting(sets) {
      console.log('applySorting() called')

      return sets.sort((set1, set2) => 
        {
          let sortDir = this.sortReverse ? -1: 1
          if (this.sortColumn === 'name') {
            return (set1.setName > set2.setName ? sortDir: -sortDir)
          }
        }
      )
    },

    viewSet(uid) {
      // Find the intervention set that matches the UID passed in.
      let matchSet = this.interventionSets.find(theSet => theSet.uid === uid)

      console.log('viewSet() called for ' + matchSet.setName)

      // Set the active intervention set to the matched intervention set.
      this.activeIntervSet = matchSet
    },

    copySet(uid) {
      // Find the intervention set that matches the UID passed in.
      let matchSet = this.interventionSets.find(theSet => theSet.uid === uid)

      console.log('copySet() called for ' + matchSet.setName)
    },

    renameSet(uid) {
      // Find the intervention set that matches the UID passed in.
      let matchSet = this.interventionSets.find(theSet => theSet.uid === uid)

      console.log('renameSet() called for ' + matchSet.setName)
    },

    deleteSet(uid) {
      // Find the intervention set that matches the UID passed in.
      let matchSet = this.interventionSets.find(theSet => theSet.uid === uid)

      console.log('deleteSet() called for ' + matchSet.setName)
    },

    createNewSet() {
      console.log('createNewSet() called')
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style lang="scss" scoped>
  .UIPlaceholder {
    height: 500px;
    width: 100%;
    border: 1px solid black;
  }

  .PHText {
    color: green;
    text-align: center;
  }
</style>
