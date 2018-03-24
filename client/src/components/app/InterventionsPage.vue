<!--
InterventionsPage.vue -- InterventionsPage Vue component

Last update: 3/23/18 (gchadder3)
-->

<template>
  <div class="SitePage">

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
          <tr v-for="intervSet in sortedFilteredIntervSets"
              :class="{ highlighted: intervSetIsSelected(intervSet) }">
            <td v-if="intervSet.renaming !== ''">
			        <input type="text"
                     class="txbox"
                     @keyup.enter="renameSet(intervSet)"
                     v-model="intervSet.renaming"/>
			      </td>
			      <td v-else>
			        {{ intervSet.intervset.name }}
			      </td>
            <td style="white-space: nowrap">
              <button class="btn __green" @click="viewSet(intervSet)">View</button>
              <button class="btn" @click="copySet(intervSet)">Copy</button>
              <button class="btn" @click="renameSet(intervSet)">Rename</button>
              <button class="btn __red" @click="deleteSet(intervSet)">Delete</button>
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

    <div class="PageSection UIPlaceholder" v-if="activeIntervSet.intervset != undefined">
<!--      <div class="PHText">
        Page interface specific to {{ activeIntervSet.intervset.name }} intervention set
      </div> -->

      <div style="margin-top: 10px">
        <table class="table table-bordered table-hover table-striped" style="width: auto">
          <thead>
            <tr>
<!--              <th>Included in optimizations</th> -->
              <th>Intervention name</th>
              <th>Type</th>
              <th>Delivery platform</th>
              <th>icer</th>
              <th>Unit cost</th>
              <th>FRP</th>
              <th>Equity</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="interv in interventionList">
<!--              <td style="text-align: center">
                <input type="checkbox" v-model="interv.included"/>
              </td> -->
              <td>{{ interv[0] }}</td>
              <td>{{ interv[3] }}</td>
              <td>{{ interv[2] }}</td>
              <td>{{ interv[4] }}</td>
              <td>{{ interv[5] }}</td>
              <td>{{ interv[6] }}</td>
              <td>{{ interv[7] }}</td>
              <td style="white-space: nowrap">
                <i class="fas fa-edit"></i>
                <i class="fas fa-copy"></i>
                <i class="fas fa-download"></i>
                <i class="fas fa-upload"></i>
                <i class="fas fa-trash-alt"></i>
              </td>
            </tr>
            <tr>
              <td>
                <button class="btn">Add new intervention</button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

<!-- Old dummy table stuff
      <div style="margin-top: 10px">
        <table id="checkboxtable" class="table table-bordered" style="width: auto">
          <tr>
            <td>
              Categories of intervention
            </td>
            <td>
              <input type="checkbox" @click="intervAllCategoryClick" v-model="showAllIntervs"/> All
            </td>
            <td>
              <input type="checkbox" v-model="showInfectiousIntervs"/> Infectious diseases
            </td>
          </tr>
          <tr>
            <td>
              to show
            </td>
            <td>
              <input type="checkbox" v-model="showCancerIntervs"/> Cancers
            </td>
            <td>
              <input type="checkbox" v-model="showChildIntervs"/> Child care
            </td>
          </tr>
        </table>
      </div>

      <div style="margin-top: 10px">
        <table class="table table-bordered table-hover table-striped" style="width: auto">
          <thead>
            <tr>
              <th>Included in optimizations</th>
              <th>Intervention name</th>
              <th>Total cost</th>
              <th>Est. DALY averted</th>
              <th>Unit cost</th>
              <th>Coverage %</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="interv in filteredInterventions">
              <td style="text-align: center">
                <input type="checkbox" v-model="interv.included"/>
              </td>
              <td>{{ interv.interventionName }}</td>
              <td></td>
              <td></td>
              <td></td>
              <td></td>
              <td>
                <i class="fas fa-edit"></i>
                <i class="fas fa-copy"></i>
                <i class="fas fa-download"></i>
                <i class="fas fa-upload"></i>
                <i class="fas fa-trash-alt"></i>
              </td>
            </tr>
            <tr>
              <td>
                <button class="btn">Add new intervention</button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <div style="margin-top: 10px">
        <span style="font-size: large">
          <i class="fas fa-download"></i> Table of all
        </span>
        &nbsp; &nbsp;
        <span style="font-size: large">
          <i class="fas fa-download"></i> Selected
        </span>
      </div> -->

    </div>
  </div>
</template>

<script>
import axios from 'axios'
var filesaver = require('file-saver')
import rpcservice from '@/services/rpc-service'
import router from '@/router'

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

/* old intervention sets stuff to get rid of
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
        ], */

      // List of objects for intervention sets the project has
      interventionSets: [],

      // Active intervention set
      activeIntervSet: {},

      // Show all of the intervention categories
      showAllIntervs: true,

      // Show cancer interventions
      showCancerIntervs: false,

      // Show infectious diseases interventions
      showInfectiousIntervs: false,

      // Show child care interventions
      showChildIntervs: false,

/* old dummy interventions used in the demo table to get rid of
      // Interventions to be shown in the table
      interventionList:
        [
          {
            interventionName: 'Skin cancer removal',
            uid: 1,
            included: true,
            intervCategory: 'cancer'
          },
          {
            interventionName: 'Brain tumor surgery',
            uid: 2,
            included: false,
            intervCategory: 'cancer'
          },
          {
            interventionName: 'TB vaccination',
            uid: 3,
            included: true,
            intervCategory: 'infectious'
          },
          {
            interventionName: 'Measles vaccination',
            uid: 4,
            included: true,
            intervCategory: 'infectious'
          },
          {
            interventionName: 'Polio vaccination',
            uid: 5,
            included: true,
            intervCategory: 'infectious'
          },
          {
            interventionName: 'Child checkup',
            uid: 6,
            included: false,
            intervCategory: 'childcare'
          }
        ] */

      interventionList: []
    }
  },

  computed: {
    activeProjectName() {
      if (this.$store.state.activeProject.project === undefined) {
        return '[nothing]'
      } else {
        return this.$store.state.activeProject.project.name
      }
    },

    sortedFilteredIntervSets() {
      return this.applyNameFilter(this.applySorting(this.interventionSets))
    },

    filteredInterventions() {
      if (this.showAllIntervs) {
        return this.interventionList
      } else {
        return this.interventionList.filter(interv =>
          {
            if (interv.intervCategory === 'cancer')
              return this.showCancerIntervs
            else if (interv.intervCategory === 'infectious')
              return this.showInfectiousIntervs
            else if (interv.intervCategory === 'childcare')
              return this.showChildIntervs
            else
              return false
          }
        )
      }
    }
  },

  created() {
    // If we have no user logged in, automatically redirect to the login page.
    if (this.$store.state.currentUser.displayname == undefined) {
      router.push('/login')
    }

    // Otherwise...
    else {
      // Load the intervention sets from the active project.
      this.updateIntervSets()
    }
  },

  methods: {
    updateIntervSets() {
      console.log('updateIntervSets() called')

      // If there is no active project, clear the interventionSets list.
      if (this.$store.state.activeProject.project === undefined) {
        this.interventionSets = []
      }

      // Otherwise...
      else {
        // Get the active project's intervention sets.
        rpcservice.rpcProjectCall('get_project_interv_sets',
          [this.$store.state.activeProject.project.id])
        .then(response => {
          // Set the intervention set list to what we received.
          this.interventionSets = response.data.intervsets

          // Add numindex elements to the intervention sets to keep track of
		      // which index to pull from the server.
          for (let ind=0; ind < this.interventionSets.length; ind++)
            this.interventionSets[ind].intervset.numindex = ind

          // Set renaming values to blank initially.
          this.interventionSets.forEach(theSet => {
		        theSet.renaming = ''
		      })
        })
      }
    },

    intervSetIsSelected(intervSet) {
      // If the active intervention set is undefined, it is not active.
      if (this.activeIntervSet.intervset === undefined) {
        return false
      }

      // Otherwise, the intervention is selected if the numindexes match.
      else {
        return (this.activeIntervSet.intervset.numindex === intervSet.intervset.numindex)
      }
    },

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
      return sets.filter(theSet => theSet.intervset.name.toLowerCase().indexOf(this.filterText.toLowerCase()) !== -1)
    },

    applySorting(sets) {
      return sets.sort((set1, set2) =>
        {
          let sortDir = this.sortReverse ? -1: 1
          if (this.sortColumn === 'name') {
            return (set1.intervset.name > set2.intervset.name ? sortDir: -sortDir)
          }
        }
      )
    },

    viewSet(intervSet) {
      console.log('viewSet() called for ' + intervSet.intervset.name)

      // Set the active intervention set to the matched intervention set.
      this.activeIntervSet = intervSet

      // Go to the server to get the interventions from the intervention set.
      rpcservice.rpcProjectCall('get_project_interv_set_intervs',
        [this.$store.state.activeProject.project.id, this.activeIntervSet.intervset.numindex])
      .then(response => {
        // Set the interventions table list.
        this.interventionList = response.data.interventions

        // Reset the bottom table sorting state.
//        this.sortColumn2 = 'name'
//        this.sortReverse2 = false
      })
    },

    copySet(intervSet) {
      console.log('copySet() called for ' + intervSet.intervset.name)

	    // Have the server copy the intervention set, giving it a new name.
      rpcservice.rpcProjectCall('copy_interv_set',
        [this.$store.state.activeProject.project.id, intervSet.intervset.numindex])
      .then(response => {
        // Update the intervention sets so the new set shows up on the list.
        this.updateIntervSets()
      })
    },

    renameSet(intervSet) {
      console.log('renameSet() called for ' + intervSet.intervset.name)

	    // If the intervention set is not in a mode to be renamed, make it so.
	    if (intervSet.renaming === '') {
		    intervSet.renaming = intervSet.intervset.name
      }

	    // Otherwise (it is to be renamed)...
	    else {
        // Have the server change the name of the intervention set.
        rpcservice.rpcProjectCall('rename_interv_set',
          [this.$store.state.activeProject.project.id,
          intervSet.intervset.numindex, intervSet.renaming])
        .then(response => {
          // Update the intervention sets so the renamed one shows up on the list.
          this.updateIntervSets()

	        // Turn off the renaming mode.
	        intervSet.renaming = ''
        })
      }

	    // This silly hack is done to make sure that the Vue component gets updated by this function call.
	    // Something about resetting the intervention set name informs the Vue component it needs to
	    // update, whereas the renaming attribute fails to update it.
	    // We should find a better way to do this.
      let theName = intervSet.intervset.name
      intervSet.intervset.name = 'newname'
      intervSet.intervset.name = theName
    },

    deleteSet(intervSet) {
      console.log('deleteSet() called for ' + intervSet.intervset.name)

      // Go to the server to delete the intervention set.
      rpcservice.rpcProjectCall('delete_interv_set',
        [this.$store.state.activeProject.project.id, intervSet.intervset.numindex])
      .then(response => {
        // Update the intervention sets so the new set shows up on the list.
        this.updateIntervSets()
      })
    },

    createNewSet() {
      console.log('createNewSet() called')

      // Go to the server to create the new intervention set.
      rpcservice.rpcProjectCall('create_interv_set',
        [this.$store.state.activeProject.project.id, 'New intervention set'])
      .then(response => {
        // Update the intervention sets so the new set shows up on the list.
        this.updateIntervSets()
      })
    },

    intervAllCategoryClick() {
      this.showCancerIntervs = false
      this.showInfectiousIntervs = false
      this.showChildIntervs = false
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style lang="scss" scoped>
  .UIPlaceholder {
//    height: 500px;
    width: 100%;
//    border: 1px solid black;
  }

  .PHText {
    color: green;
    text-align: center;
  }

  #checkboxtable td {
    padding: 0px 5px;
  }
</style>
