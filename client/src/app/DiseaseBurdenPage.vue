<!--
Define disease burden

Last update: 2018sep24
-->

<template>
  <div class="SitePage">

    <div v-if="activeProjectName === ''">
      <div style="font-style:italic">
        <p>Hmm, I can't find any disease burdens...did you forget to load a project?</p>
      </div>
    </div>

    <div class="PageSection" v-if="activeProjectName !== ''">
      <button class="btn" @click="createNewBurdenSet">Create new burden set</button>

      <span>&nbsp;based on&nbsp;</span>
      <select
        title="countrySelect"
        id="country"
        :required="true"
        v-model="country">
        <option v-for = "country in countryList" :value="country">
          {{country}}
        </option>
      </select>

      <br/><br/>

      <input type="text"
             class="txbox"
             style="margin-left:0px; margin-bottom:10px; display:inline-block; width:100%"
             :placeholder="filterPlaceholder"
             v-model="filterText"/>

      <table class="table table-bordered table-hover table-striped" style="width: 100%">
        <thead>
          <tr>
            <th @click="updateSorting('name')" class="sortable">
              Burden set
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
            <th>
              Select
            </th>
            <th @click="updateSorting('creationTime')" class="sortable">
              Created on
              <span v-show="sortColumn == 'creationTime' && !sortReverse">
                <i class="fas fa-caret-down"></i>
              </span>
              <span v-show="sortColumn == 'creationTime' && sortReverse">
                <i class="fas fa-caret-up"></i>
              </span>
              <span v-show="sortColumn != 'creationTime'">
                <i class="fas fa-caret-up" style="visibility: hidden"></i>
              </span>
            </th>
            <th @click="updateSorting('updatedTime')" class="sortable">
              Last modified
              <span v-show="sortColumn == 'updatedTime' && !sortReverse">
                <i class="fas fa-caret-down"></i>
              </span>
              <span v-show="sortColumn == 'updatedTime' && sortReverse">
                <i class="fas fa-caret-up"></i>
              </span>
              <span v-show="sortColumn != 'updatedTime'">
                <i class="fas fa-caret-up" style="visibility: hidden"></i>
              </span>
            </th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="burdenSet in sortedFilteredBurdenSets"
              :class="{ highlighted: burdenSetIsSelected(burdenSet) }">
            <td v-if="burdenSet.renaming !== ''">
			        <input type="text"
                     class="txbox"
                     @keyup.enter="renameBurdenSet(burdenSet)"
                     v-model="burdenSet.renaming"/>
			      </td>
			      <td v-else>
			        {{ burdenSet.burdenset.name }}
			      </td>
            <td><button class="btn __green" @click="viewBurdenSet(burdenSet, true)">Open</button></td>
            <td>{{ burdenSet.burdenset.creationTime }}</td>
            <td>{{ burdenSet.burdenset.updateTime ? burdenSet.burdenset.updateTime:
              'No modification' }}</td>
            <td style="white-space: nowrap">
              <button class="btn" @click="renameBurdenSet(burdenSet)">Rename</button>
              <button class="btn" @click="copyBurdenSet(burdenSet)">Copy</button>
              <button class="btn" @click="uploadBurdenSet(burdenSet)">Upload</button>
              <button class="btn" @click="downloadBurdenSet(burdenSet)">Download</button>
              <button class="btn __red" @click="deleteBurdenSet(burdenSet)">Delete</button>
            </td>
          </tr>
        </tbody>
      </table>
      <button v-show="!showingPlots" class="btn" :disabled="!graphData" @click="showPlots">Show plots</button>
      <button v-show="showingPlots"  class="btn" :disabled="!graphData" @click="hidePlots">Hide plots</button>
      <button class="btn" :disabled="!graphData" @click="downloadPlots">Download plots</button>
    </div>

    <div class="PageSection UIPlaceholder" v-if="activeBurdenSet.burdenset != undefined">

      <div v-show="showingPlots">
        <div id="fig1" style="float:left" ></div>
        <div id="fig2" style="float:left" ></div>
        <div id="fig3" style="float:left" ></div>
      </div>

      <input type="text"
             class="txbox"
             style="margin-left:0px; margin-bottom:10px; display:inline-block; width:100%"
             :placeholder="filterPlaceholder2"
             v-model="filterText2"/>

      <table class="table table-bordered table-hover table-striped scrolltable" style="width: 100%; margin-top: 10px;">
        <thead>
          <tr>
            <th style="text-align:center">
              Active
            </th>
            <th @click="updateSorting2('name')" class="sortable">
              Cause name
              <span v-show="sortColumn2 == 'name' && !sortReverse2">
                <i class="fas fa-caret-down"></i>
              </span>
              <span v-show="sortColumn2 == 'name' && sortReverse2">
                <i class="fas fa-caret-up"></i>
              </span>
              <span v-show="sortColumn2 != 'name'">
                <i class="fas fa-caret-up" style="visibility: hidden"></i>
              </span>
            </th>
            <th @click="updateSorting2('DALYs')" class="sortable">
              DALYs
              <span v-show="sortColumn2 == 'DALYs' && !sortReverse2">
                <i class="fas fa-caret-down"></i>
              </span>
              <span v-show="sortColumn2 == 'DALYs' && sortReverse2">
                <i class="fas fa-caret-up"></i>
              </span>
              <span v-show="sortColumn2 != 'DALYs'">
                <i class="fas fa-caret-up" style="visibility: hidden"></i>
              </span>
            </th>
            <th @click="updateSorting2('deaths')" class="sortable">
              Deaths
              <span v-show="sortColumn2 == 'deaths' && !sortReverse2">
                <i class="fas fa-caret-down"></i>
              </span>
              <span v-show="sortColumn2 == 'deaths' && sortReverse2">
                <i class="fas fa-caret-up"></i>
              </span>
              <span v-show="sortColumn2 != 'deaths'">
                <i class="fas fa-caret-up" style="visibility: hidden"></i>
              </span>
            </th>
            <th @click="updateSorting2('prevalence')" class="sortable">
              Prevalence
              <span v-show="sortColumn2 == 'prevalence' && !sortReverse2">
                <i class="fas fa-caret-down"></i>
              </span>
              <span v-show="sortColumn2 == 'prevalence' && sortReverse2">
                <i class="fas fa-caret-up"></i>
              </span>
              <span v-show="sortColumn2 != 'prevalence'">
                <i class="fas fa-caret-up" style="visibility: hidden"></i>
              </span>
            </th>
            <th style="text-align:center">Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="disease in sortedFilteredDiseases">
            <td style="text-align: center">
              <input type="checkbox"
                     v-model="disease['Active']"/>
            </td>
            <td>
              <input type="text"
                     class="txbox"
                     @keyup.enter="updateDisease(disease)"
                     v-model="disease['Cause']"/>
            </td>
            <td>
              <input type="text"
                     class="txbox"
                     @keyup.enter="updateDisease(disease)"
                     v-model="disease['DALYs']"/>
            </td>
            <td>
              <input type="text"
                     class="txbox"
                     @keyup.enter="updateDisease(disease)"
                     v-model="disease['Deaths']"/>
            </td>
            <td>
              <input type="text"
                     class="txbox"
                     @keyup.enter="updateDisease(disease)"
                     v-model="disease['Prevalence']"/>
            </td>
            <td style="white-space: nowrap">
              <button class="iconbtn" @click="copyBurden(disease)" data-tooltip="Copy burden"><i class="ti-layers"></i></button>
              <button class="iconbtn" @click="deleteBurden(disease)" data-tooltip="Delete burden"><i class="ti-trash"></i></button>
            </td>
          </tr>
        </tbody>
      </table>
      <button class="btn" @click="addBurden">Add new burden</button>

    </div>
  </div>
</template>

<script>
  import axios from 'axios'
  var filesaver = require('file-saver')
  import status from '@/js/status-service'
  import rpcs from '@/js/rpc-service'
  import utils from '@/js/utils'
  import router from '@/router'
  import Vue from 'vue';

  export default {
    name: 'DiseaseBurdenPage',

    data() {
      return {
        filterPlaceholder: 'Type here to filter burden sets', // Placeholder text for first table filter box
        filterPlaceholder2: 'Type here to filter diseases (cause names)', // Placeholder text for second table filter box
        filterText: '', // Text in the first table filter box
        filterText2: '', // Text in the second table filter box
        sortColumn: 'updatedTime',  // Column of table used for sorting the burden sets // name, creationTime, updatedTime
        sortReverse: false, // Sort in reverse order?
        burdenSets: [], // List of burden sets in the active project
        activeBurdenSet: {}, // Active burden set
        diseaseList: [], // List of diseases.  Each list element is a list of the ailment name and numbers associated with it.
        sortColumn2: 'name',  // Column of table used for sorting the diseases
        sortReverse2: false, // Sort diseases in reverse order?
        country: 'Afghanistan',
        countryList: [
          'Afghanistan',
          'Argentina',
          'Cambodia',
          "Cote d'Ivoire",
          'Zimbabwe',
        ],
        showingPlots: false,
        graphData: [],
      }
    },

    computed: {
      activeProjectName() {
        if (this.$store.state.activeProject.project === undefined) {
          return ''
        } else {
          return this.$store.state.activeProject.project.name
        }
      },

      sortedFilteredBurdenSets() {
        return this.applyNameFilter(this.applySorting(this.burdenSets))
      },

      sortedFilteredDiseases() {
        return this.applyDiseaseFilter(this.applySorting2(this.diseaseList))
      }     
    },

    created() {
      if (this.$store.state.currentUser.displayname === undefined) { // If we have no user logged in, automatically redirect to the login page.
        router.push('/login')
      } else { // Otherwise...
        this.updateBurdenSets(true) // Load the burden sets from the active project, telling the function to also set the active burden set to the last item.
      }
    },

    methods: {

      notImplemented() {
        status.fail(this, 'This feature is not implemented')
      },

      clearGraphs(numfigs) { return utils.clearGraphs(this, numfigs)},

      showPlots() {
        this.showingPlots = true
      },

      hidePlots() {
        this.showingPlots = false
      },

      downloadPlots() {
        rpcs.download('download_figures', [this.$store.state.currentUser.username])
          .then(response => {
            console.log('Downloaded figures')
          })
      },

      updateBurdenSets(setLastEntryActive) {
        console.log('updateBurdenSets() called')
        if (this.$store.state.activeProject.project === undefined) { // If there is no active project, clear the burdenSets list.
          this.burdenSets = []
        } else { // Otherwise...
          rpcs.rpc('jsonify_burdensets', [this.$store.state.activeProject.project.id]) // Get the active project's burden sets.
          .then(response => {
            this.burdenSets = response.data.burdensets // Set the burden set list to what we received.
            for (let ind=0; ind < this.burdenSets.length; ind++) { // Add numindex elements to the burden sets to keep track of which index to pull from the server.
              this.burdenSets[ind].burdenset.numindex = ind
            }
            this.burdenSets.forEach(theSet => { // Set renaming values to blank initially.
		          theSet.renaming = ''
		        })
            if ((setLastEntryActive) && (this.burdenSets.length > 0)) { // If we want to set the last entry active and we have any entries, do the setting.
              this.viewBurdenSet(this.burdenSets[this.burdenSets.length - 1])
            }
          })
        }
      },

      burdenSetIsSelected(burdenSet) {
        if (this.activeBurdenSet.burdenset === undefined) { // If the active burden set is undefined, it is not active.
          return false
        } else { // Otherwise, the burden set is selected if the numindexes match.
          return (this.activeBurdenSet.burdenset.numindex === burdenSet.burdenset.numindex)
        }
      },

      updateSorting(sortColumn) {
        console.log('updateSorting() called')
        if (this.sortColumn === sortColumn) { // If the active sorting column is clicked...
            this.sortReverse = !this.sortReverse // Reverse the sort.
        } else { // Otherwise.
          this.sortColumn = sortColumn // Select the new column for sorting.
          this.sortReverse = false // Set the sorting for non-reverse.
        }
      },

      applyNameFilter(sets) {
        console.log(sets)
        return sets.filter(theSet => theSet.burdenset.name.toLowerCase().indexOf(this.filterText.toLowerCase()) !== -1)
      },

      applySorting(sets) {
        return sets.sort((set1, set2) =>
          {
            let sortDir = this.sortReverse ? -1: 1
            if      (this.sortColumn === 'name')         {return (set1.burdenset.name         > set2.burdenset.name         ? sortDir: -sortDir)}
            else if (this.sortColumn === 'creationTime') {return (set1.burdenset.creationTime > set2.burdenset.creationTime ? sortDir: -sortDir)}
            else if (this.sortColumn === 'updatedTime')  {return (set1.burdenset.updateTime   > set2.burdenset.updateTime   ? sortDir: -sortDir)}
          }
        )
      },

      viewBurdenSet(burdenSet, verbose) {
        console.log('viewBurdenSet() called for ' + burdenSet.burdenset.name)
        this.activeBurdenSet = burdenSet // Set the active project to the burdenSet passed in.
        rpcs.rpc('jsonify_diseases', [this.$store.state.activeProject.project.id, this.activeBurdenSet.burdenset.numindex]) // Go to the server to get the diseases from the burden set.
        .then(response => {
          this.diseaseList = response.data.diseases // Set the disease list.
          for (let ind=0; ind < this.diseaseList.length; ind++) { // Set the active values from the loaded in data.
            this.diseaseList[ind].numindex = ind
		        this.diseaseList[ind]['Active'] = (this.diseaseList[ind][0] > 0)
            this.diseaseList[ind]['Cause'] = this.diseaseList[ind][1]
            this.diseaseList[ind]['DALYs'] = Number(this.diseaseList[ind][2]).toLocaleString()
            this.diseaseList[ind]['Deaths'] = Number(this.diseaseList[ind][3]).toLocaleString()
            this.diseaseList[ind]['Prevalence'] = Number(this.diseaseList[ind][4]).toLocaleString()
		      }
          this.sortColumn2 = 'name' // Reset the bottom table sorting state.
          this.sortReverse2 = false
          this.makeGraph(burdenSet) // Plot graphs
        })
          .catch(error => {
            status.fail(this, 'Could not update burden sets', error)
          })
        if (verbose) {
          status.succeed(this, 'Burden set "' + burdenSet.burdenset.name + '" now active')
        }
      },

      makeGraph(burdenSet) {
        console.log('makeGraph() called for ' + burdenSet.burdenset.name)
        this.activeBurdenSet = burdenSet // Set the active project to the matched project.
        this.clearGraphs(3)
        rpcs.rpc('plot_burden',  // Go to the server to get the diseases from the burden set.
          [this.$store.state.activeProject.project.id, this.activeBurdenSet.burdenset.numindex])
          .then(response => {
            this.graphData = response.data
            if (this.graphData) { // Check we got a response
              mpld3.draw_figure('fig1', this.graphData.graph1) // Draw the figure.
              mpld3.draw_figure('fig2', this.graphData.graph2) // Draw the figure.
              mpld3.draw_figure('fig3', this.graphData.graph3) // Draw the figure.
            }
          })
          .catch(error => {
            status.fail(this, 'Could not make graphs', error)
          })
      },

      copyBurdenSet(burdenSet) {
        console.log('copyBurdenSet() called for ' + burdenSet.burdenset.name)
        rpcs.rpc('copy_set', [this.$store.state.activeProject.project.id, 'burdenset', burdenSet.burdenset.numindex]) // Have the server copy the burden set, giving it a new name.
        .then(response => {
          this.updateBurdenSets() // Update the burden sets so the new set shows up on the list.
        })
      },

      uploadBurdenSet(burdenSet) {
        console.log('uploadBurdenSet() called for ' + burdenSet.burdenset.name)
        rpcs.upload('upload_set', [this.$store.state.activeProject.project.id, 'burdenset', burdenSet.burdenset.numindex], {}, '.xlsx')
          .then(response => {
            this.updateBurdenSets()
            this.viewBurdenSet(burdenSet, true)
            status.succeed(this, 'Burden set uploaded')
          })
          .catch(error => {
            status.fail(this, 'Could not upload burden set', error)
          })

      },

      downloadBurdenSet(burdenSet) {
        console.log('downloadBurdenSet() called for ' + burdenSet.burdenset.name)
        rpcs.download('download_set', [this.$store.state.activeProject.project.id, 'burdenset', burdenSet.burdenset.numindex])
          .then(response => {
            console.log('Downloaded')
          })
          .catch(error => {
            status.fail(this, 'Could not download burden set', error)
          })
      },

      renameBurdenSet(burdenSet) {
        console.log('renameBurdenSet() called for ' + burdenSet.burdenset.name)
	      if (burdenSet.renaming === '') { // If the burden set is not in a mode to be renamed, make it so.
		      burdenSet.renaming = burdenSet.burdenset.name
        } else { // Otherwise (it is to be renamed)...
          rpcs.rpc('rename_set', [this.$store.state.activeProject.project.id, 'burdenset', burdenSet.burdenset.numindex, burdenSet.renaming]) // Have the server change the name of the burden set.
          .then(response => {
            this.updateBurdenSets() // Update the burden sets so the renamed one shows up on the list.
		        burdenSet.renaming = '' // Turn off the renaming mode.
          })
        }

	      // This silly hack is done to make sure that the Vue component gets updated by this function call.
	      // Something about resetting the burden set name informs the Vue component it needs to
	      // update, whereas the renaming attribute fails to update it.
	      // We should find a better way to do this.
        let theName = burdenSet.burdenset.name
        burdenSet.burdenset.name = 'newname'
        burdenSet.burdenset.name = theName
      },

      deleteBurdenSet(burdenSet) {
        console.log('deleteBurdenSet() called for ' + burdenSet.burdenset.name)
        rpcs.rpc('delete_set', [this.$store.state.activeProject.project.id, 'burdenset', burdenSet.burdenset.numindex]) // Go to the server to delete the burden set.
        .then(response => {
          this.updateBurdenSets() // Update the burden sets so the new set shows up on the list.
        })
      },

      createNewBurdenSet() {
        console.log('createNewBurdenSet() called')
        rpcs.rpc('create_burdenset', [this.$store.state.activeProject.project.id, this.country]) // Go to the server to create the new burden set.
          .then(response => {
          this.updateBurdenSets() // Update the burden sets so the new set shows up on the list.
        })
      },

      updateSorting2(sortColumn) {
        console.log('updateSorting2() called')
        // If the active sorting column is clicked...
        if (this.sortColumn2 === sortColumn) {
            this.sortReverse2 = !this.sortReverse2 // Reverse the sort.
        } else { // Otherwise.
          this.sortColumn2 = sortColumn // Select the new column for sorting.
          this.sortReverse2 = false // Set the sorting for non-reverse.
        }
      },
      
      applyDiseaseFilter(diseases) {
        console.log(diseases)
        return diseases.filter(theDisease => theDisease['Cause'].toLowerCase().indexOf(this.filterText2.toLowerCase()) !== -1)
      },
      
      applySorting2(diseases) {
        return diseases.sort((disease1, disease2) =>
          {
            let sortDir = this.sortReverse2 ? -1: 1
            if      (this.sortColumn2 === 'name')       {return (disease1[1] > disease2[1] ? sortDir: -sortDir)}
            else if (this.sortColumn2 === 'DALYs')      {return disease1[2] > disease2[2] ? sortDir: -sortDir}
            else if (this.sortColumn2 === 'deaths')     {return disease1[3] > disease2[3] ? sortDir: -sortDir}
            else if (this.sortColumn2 === 'prevalence') {return disease1[4] > disease2[4] ? sortDir: -sortDir}
          }
        )
      },

      updateDisease(disease) {
        console.log('Update to be made')
        console.log('Index: ',      disease.numindex)
        console.log('Active?: ',    disease['Active'])
        console.log('Cause: ',      disease['Cause'])
        console.log('DALYs: ',      disease['DALYs'])
        console.log('Deaths: ',     disease['Deaths'])
        console.log('Prevalence: ', disease['Prevalence'])

        // Do format filtering to prepare the data to pass to the RPC.
        let filterActive = disease['Active'] ? 1 : 0

        // Go to the server to update the disease from the burden set. Note: filter out commas in the numeric fields.
        rpcs.rpc('update_disease', [this.$store.state.activeProject.project.id, this.activeBurdenSet.burdenset.numindex, disease.numindex,
          [disease['Active'], disease['Cause'], disease['DALYs'], disease['Deaths'], disease['Prevalence']]])
        .then(response => {
          status.succeed(this, 'Burden set updated')
        })
      },

      addBurden() {
        console.log('Adding burden')
        rpcs.rpc('add_burden', [this.$store.state.activeProject.project.id, this.activeBurdenSet.burdenset.numindex])
          .then(response => {
            this.viewBurdenSet(this.activeBurdenSet) // Update the display of the burden list by rerunning the active burden set.
            status.succeed(this, 'Burden added')
          })
      },

      copyBurden(burden) {
        console.log('Item to copy:', burden.numindex)
        rpcs.rpc('copy_burden', [this.$store.state.activeProject.project.id, this.activeBurdenSet.burdenset.numindex, burden.numindex])
          .then(response => {
            this.viewBurdenSet(this.activeBurdenSet) // Update the display of the burden list by rerunning the active burden set.
            status.succeed(this, 'Burden copied')
          })
      },

      deleteBurden(burden) {
        console.log('Item to delete:', burden.numindex)
        rpcs.rpc('delete_burden', [this.$store.state.activeProject.project.id, this.activeBurdenSet.burdenset.numindex, burden.numindex])
          .then(response => {
            this.viewBurdenSet(this.activeBurdenSet) // Update the display of the burden list by rerunning the active burden set.
            status.succeed(this, 'Burden deleted')
          })
      },

    }
  }
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style lang="scss" scoped>

</style>
