<!--
Define health packages

Last update: 2018-09-24
-->

<template>
  <div class="SitePage">

    <div v-if="activeProjectName === ''">
      <div style="font-style:italic">
        <p>Hmm, I can't find any health packages...did you forget to <router-link to="/projects">load a project</router-link>?</p>
      </div>
    </div>

    <div class="PageSection" v-if="activeProjectName !== ''">

      <div v-if="burdenSet">
        <button class="btn" @click="createNewPackageSet">Create health package</button>
        &nbsp;Burden set:&nbsp;
        <select v-model="burdenSet">
          <option v-for='set in burdenSets'>
            {{ set }}
          </option>
        </select>
        &nbsp;Intervention set:&nbsp;
        <select v-model="intervSet">
          <option v-for='set in intervSets'>
            {{ set }}
          </option>
        </select>
        <br><br>
      </div>


      <div v-if="packageSets">

        <input type="text"
               class="txbox"
               style="margin-left:0px; margin-bottom:10px; display:inline-block; width:100%"
               :placeholder="filterPlaceholder"
               v-model="filterText"/>

        <table class="table table-bordered table-hover table-striped" style="width: 100%">
          <thead>
          <tr>
            <th @click="updateSorting('name')" class="sortable">
              Health package
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
          <tr v-for="packageSet in sortedFilteredPackageSets"
              :class="{ highlighted: packageSetIsSelected(packageSet) }">
            <td v-if="packageSet.renaming !== ''">
              <input type="text"
                     class="txbox"
                     @keyup.enter="renamePackageSet(packageSet)"
                     v-model="packageSet.renaming"/>
            </td>
            <td v-else>
              {{ packageSet.packageset.name }}
            </td>
            <td><button class="btn __green" @click="viewPackageSet(packageSet)">Open</button></td>
            <td>{{ packageSet.packageset.creationTime }}</td>
            <td>{{ packageSet.packageset.updateTime ? packageSet.packageset.updateTime:
              'No modification' }}</td>
            <td style="white-space: nowrap">
              <button class="btn" @click="renamePackageSet(packageSet)">Rename</button>
              <button class="btn" @click="copyPackageSet(packageSet)">Copy</button>
              <button class="btn" @click="downloadPackageSet(packageSet)">Download</button>
              <button class="btn __red" @click="deletePackageSet(packageSet)">Delete</button>
            </td>
          </tr>
          </tbody>
        </table>
      </div>

    </div>

    <div class="PageSection UIPlaceholder" v-if="activePackageSet.packageset != undefined">

      <table>
        <tr>
          <td><b>Budget:</b>&nbsp;</td>
          <td><input type="text"
                     class="txbox"
                     v-model="budget"/></td>
        <!--</tr>-->
        <!--<tr>-->
          <td><b>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;FRP weight:</b>&nbsp;</td>
          <td><input type="text"
                     class="txbox"
                     v-model="frpwt"/></td>
        <!--</tr>-->
        <!--<tr>-->
          <td><b>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Equity weight:</b>&nbsp;</td>
          <td><input type="text"
                     class="txbox"
                     v-model="equitywt"/></td>
        </tr>

      </table>
      <br>

      <button class="btn" @click="optimize">Optimize</button>
      <button v-show="!showingPlots" class="btn" @click="showPlots">Show plots</button>
      <button v-show="showingPlots" class="btn" @click="hidePlots">Hide plots</button>
      <button class="btn" @click="downloadPlots">Download plots</button>
    </div>

    <div class="PageSection UIPlaceholder" v-if="activePackageSet.packageset != undefined">

      <div v-show="showingPlots">
        <div id="fig1" style="float:left" ></div>
        <div id="fig2" style="float:left" ></div>
        <div id="fig3" style="float:left" ></div>
        <div id="fig4" style="float:left" ></div>
        <div id="fig5" style="float:left" ></div>
      </div>

      <input type="text"
             class="txbox"
             style="margin-left:0px; margin-bottom:10px; display:inline-block; width:100%"
             :placeholder="filterPlaceholder2"
             v-model="filterText2"/>

      <table class="table table-bordered table-hover table-striped scrolltable" style="width: 100%; margin-top: 10px;">
        <thead>
        <tr>
          <th @click="updateSorting2('name')" class="sortable">Intervention
            <span v-show="sortColumn2 == 'name' && !sortReverse2"><i class="fas fa-caret-down"></i></span>
            <span v-show="sortColumn2 == 'name' && sortReverse2"><i class="fas fa-caret-up"></i></span>
            <span v-show="sortColumn2 != 'name'"><i class="fas fa-caret-up" style="visibility: hidden"></i></span>
          </th>
          <th @click="updateSorting2('cause')" class="sortable">Cause&nbsp;of&nbsp;burden
            <span v-show="sortColumn2 == 'cause' && !sortReverse2"><i class="fas fa-caret-down"></i></span>
            <span v-show="sortColumn2 == 'cause' && sortReverse2"><i class="fas fa-caret-up"></i></span>
            <span v-show="sortColumn2 != 'cause'"><i class="fas fa-caret-up" style="visibility: hidden"></i></span>
          </th>
          <th @click="updateSorting2('spend')" class="sortable">Spending
            <span v-show="sortColumn2 == 'spend' && !sortReverse2"><i class="fas fa-caret-down"></i></span>
            <span v-show="sortColumn2 == 'spend' && sortReverse2"><i class="fas fa-caret-up"></i></span>
            <span v-show="sortColumn2 != 'spend'"><i class="fas fa-caret-up" style="visibility: hidden"></i></span>
          </th>
          <th @click="updateSorting2('opt_spend')" class="sortable">Optimized&nbsp;spending
            <span v-show="sortColumn2 == 'opt_spend' && !sortReverse2"><i class="fas fa-caret-down"></i></span>
            <span v-show="sortColumn2 == 'opt_spend' && sortReverse2"><i class="fas fa-caret-up"></i></span>
            <span v-show="sortColumn2 != 'opt_spend'"><i class="fas fa-caret-up" style="visibility: hidden"></i></span>
          </th>
          <th @click="updateSorting2('averted')" class="sortable">DALYs&nbsp;averted
            <span v-show="sortColumn2 == 'averted' && !sortReverse2"><i class="fas fa-caret-down"></i></span>
            <span v-show="sortColumn2 == 'averted' && sortReverse2"><i class="fas fa-caret-up"></i></span>
            <span v-show="sortColumn2 != 'averted'"><i class="fas fa-caret-up" style="visibility: hidden"></i></span>
          </th>
          <th @click="updateSorting2('opt_averted')" class="sortable">Optimized&nbsp;DALYs&nbsp;averted
            <span v-show="sortColumn2 == 'opt_averted' && !sortReverse2"><i class="fas fa-caret-down"></i></span>
            <span v-show="sortColumn2 == 'opt_averted' && sortReverse2"><i class="fas fa-caret-up"></i></span>
            <span v-show="sortColumn2 != 'opt_averted'"><i class="fas fa-caret-up" style="visibility: hidden"></i></span>
          </th>
        </tr>
        </thead>
        <tbody>
        <tr v-for="result in sortedFilteredIntervs">
          <td>{{ result.name }}</td>
          <td>{{ result.cause }}</td>
          <td>{{ result.spend }}</td>
          <td>{{ result.opt_spend }}</td>
          <td>{{ result.averted }}</td>
          <td>{{ result.opt_averted }}</td>
        </tr>
        </tbody>
      </table>

    </div>
  </div>
</template>

<script>
  import axios from 'axios'
  var filesaver = require('file-saver')
  import rpcs from '@/js/rpc-service'
  import status from '@/js/status-service'
  import router from '@/router'
  import utils from '@/js/utils'
  import Vue from 'vue';

  export default {
    name: 'HealthPackagesPage',

    data() {
      return {
        filterPlaceholder: 'Type here to filter health packages', // Placeholder text for first table filter box
        filterPlaceholder2: 'Type here to filter interventions', // Placeholder text for second table filter box
        filterText: '', // Text in the first table filter box
        filterText2: '', // Text in the second table filter box
        sortColumn: 'updatedTime',  // Column of table used for sorting the health package sets // name, creationTime, updatedTime
        sortReverse: false, // Sort in reverse order?
        packageSets: [], // List of health package sets in the active project
        activePackageSet: {}, // Active health package set
        resultList: [], // List of diseases.  Each list element is a list of the ailment name and numbers associated with it.
        sortColumn2: 'name',  // Column of table used for sorting the diseases // name, country, creationTime, updatedTime
        sortReverse2: true, // Sort diseases in reverse order?
        serverresponse: 'no response',
        showingPlots: false,
        burdenSet: '',
        burdenSets: [],
        intervSet: '',
        intervSets: [],
        budget: '',
        frpwt: '',
        equitywt: '',
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

      sortedFilteredPackageSets() {
        return this.applyNameFilter(this.applySorting(this.packageSets))
      },

      sortedFilteredIntervs() {
        return this.applyIntervFilter(this.applySorting2(this.resultList))
      }
    },

    created() {
      if (this.$store.state.currentUser.displayname === undefined) { // If we have no user logged in, automatically redirect to the login page.
        router.push('/login')
      } else { // Otherwise...
        this.updatePackageSets(true) // Load the health package sets from the active project, telling the function to also set the active health package set to the last item.
      }
    },

    methods: {

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

      optimize() {
        rpcs.rpc('optimize', [this.$store.state.activeProject.project.id, this.activePackageSet.packageset.numindex, this.budget, this.frpwt, this.equitywt])
          .then(response => {
            this.updatePackageSets(true)
            status.update(this, 'Optimized')
            console.log('Optimized')
          })
      },

      updatePackageSets(setLastEntryActive) {
        console.log('updatePackageSets() called')
        if (this.$store.state.activeProject.project === undefined) { // If there is no active project, clear the packageSets list.
          this.packageSets = []
        } else { // Otherwise...
          rpcs.rpc('jsonify_packagesets', [this.$store.state.activeProject.project.id]) // Get the active project's health package sets.
            .then(response => {
              this.packageSets = response.data.packagesets // Set the package set list to what we received.
              this.burdenSets = response.data.burdensets
              this.intervSets = response.data.intervsets
              this.burdenSet = this.burdenSets[0]
              this.intervSet = this.intervSets[0]
              for (let ind=0; ind < this.packageSets.length; ind++) { // Add numindex elements to the package sets to keep track of which index to pull from the server.
                this.packageSets[ind].packageset.numindex = ind
              }
              this.packageSets.forEach(theSet => { // Set renaming values to blank initially.
                theSet.renaming = ''
              })
              if ((setLastEntryActive) && (this.packageSets.length > 0)) { // If we want to set the last entry active and we have any entries, do the setting.
                this.viewPackageSet(this.packageSets[this.packageSets.length - 1])
              }
            })
            .catch(error => {
              status.fail(this, 'Could not get package sets', error)
            })
        }
      },

      packageSetIsSelected(packageSet) {
        if (this.activePackageSet.packageset === undefined) { // If the active package set is undefined, it is not active.
          return false
        } else { // Otherwise, the package set is selected if the numindexes match.
          return (this.activePackageSet.packageset.numindex === packageSet.packageset.numindex)
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
        return sets.filter(theSet => theSet.packageset.name.toLowerCase().indexOf(this.filterText.toLowerCase()) !== -1)
      },

      applySorting(sets) {
        return sets.sort((set1, set2) =>
          {
            let sortDir = this.sortReverse ? -1: 1
            if (this.sortColumn === 'name') {
              return (set1.packageset.name > set2.packageset.name ? sortDir: -sortDir)
            }
            else if (this.sortColumn === 'creationTime') {
              return set1.packageset.creationTime > set2.packageset.creationTime ? sortDir: -sortDir
            }
            else if (this.sortColumn === 'updatedTime') {
              return set1.packageset.updateTime > set2.packageset.updateTime ? sortDir: -sortDir
            }
          }
        )
      },

      viewPackageSet(packageSet) {
        console.log('viewPackageSet() called for ' + packageSet.packageset.name)
        this.activePackageSet = packageSet // Set the active project to the packageSet passed in.
        rpcs.rpc('jsonify_packages', [this.$store.state.activeProject.project.id, this.activePackageSet.packageset.numindex]) // Go to the server to get the diseases from the package set.
          .then(response => {
            this.budget = Math.round(Number(response.data.budget)).toLocaleString()
            this.frpwt = response.data.frpwt
            this.equitywt = response.data.equitywt
            this.resultList = response.data.results // Set the result list.
            for (let ind=0; ind < this.resultList.length; ind++) { // Set the active values from the loaded in data.
              this.resultList[ind].numindex =   ind
              this.resultList[ind].name =         this.resultList[ind][0]
              this.resultList[ind].cause =        this.resultList[ind][1]
              this.resultList[ind].spend =     Math.round(Number(this.resultList[ind][2])).toLocaleString()
              this.resultList[ind].opt_spend = Math.round(Number(this.resultList[ind][3])).toLocaleString()
              this.resultList[ind].averted =      Math.round(Number(this.resultList[ind][4])).toLocaleString()
              this.resultList[ind].opt_averted =  Math.round(Number(this.resultList[ind][5])).toLocaleString()
            }
            this.sortColumn2 = 'name' // Reset the bottom table sorting state.
            this.sortReverse2 = false
            this.makeGraph(packageSet) // Plot graphs
          })
          .catch(error => {
            status.fail(this, 'Could not view health package sets', error)
          })
        status.succeed(this, 'Health package "' + packageSet.packageset.name + '" now active')
      },

      makeGraph(packageSet) {
        console.log('makeGraph() called for ' + packageSet.packageset.name)
        this.activePackageSet = packageSet // Set the active project to the matched project.
        this.clearGraphs(5)
        rpcs.rpc('plot_packages', [this.$store.state.activeProject.project.id, this.activePackageSet.packageset.numindex]) // Go to the server to get the results from the package set.
          .then(response => {
            mpld3.draw_figure('fig1', response.data.graph1) // Draw the figure.
            mpld3.draw_figure('fig2', response.data.graph2) // Draw the figure.
            mpld3.draw_figure('fig3', response.data.graph3) // Draw the figure.
            mpld3.draw_figure('fig4', response.data.graph4) // Draw the figure.
            mpld3.draw_figure('fig5', response.data.graph5) // Draw the figure.
          })
          .catch(error => {
            status.fail(this, 'Could not make graphs', error)
          })
      },

      copyPackageSet(packageSet) {
        console.log('copyPackageSet() called for ' + packageSet.packageset.name)
        rpcs.rpc('copy_set', [this.$store.state.activeProject.project.id, 'packageset', packageSet.packageset.numindex]) // Have the server copy the package set, giving it a new name.
          .then(response => {
            this.updatePackageSets() // Update the package sets so the new set shows up on the list.
          })
      },

      uploadPackageSet(packageSet) {
        console.log('uploadPackageSet() called for ' + packageSet.packageset.name)
        rpcs.upload('upload_set', [this.$store.state.activeProject.project.id, 'packageset', packageSet.packageset.numindex], {}, '.xlsx')
          .then(response => {
            this.updatePackageSets()
            status.succeed(this, 'Package set uploaded')
          })
          .catch(error => {
            status.fail(this, 'Could not upload package set', error)
          })
      },

      downloadPackageSet(packageSet) {
        console.log('downloadPackageSet() called for ' + packageSet.packageset)
        rpcs.download('download_set', [this.$store.state.activeProject.project.id, 'packageset', packageSet.packageset.numindex])
          .then(response => {
            console.log('Downloaded')
          })
      },

      renamePackageSet(packageSet) {
        console.log('renamePackageSet() called for ' + packageSet.packageset.name)
        if (packageSet.renaming === '') { // If the package set is not in a mode to be renamed, make it so.
          packageSet.renaming = packageSet.packageset.name
        } else { // Otherwise (it is to be renamed)...
          rpcs.rpc('rename_set', [this.$store.state.activeProject.project.id, 'packageset', packageSet.packageset.numindex, packageSet.renaming]) // Have the server change the name of the package set.
            .then(response => {
              this.updatePackageSets() // Update the package sets so the renamed one shows up on the list.
              packageSet.renaming = '' // Turn off the renaming mode.
            })
        }

        // This silly hack is done to make sure that the Vue component gets updated by this function call.
        // Something about resetting the package set name informs the Vue component it needs to
        // update, whereas the renaming attribute fails to update it.
        // We should find a better way to do this.
        let theName = packageSet.packageset.name
        packageSet.packageset.name = 'newname'
        packageSet.packageset.name = theName
      },

      deletePackageSet(packageSet) {
        console.log('deletePackageSet() called for ' + packageSet.packageset.name)
        rpcs.rpc('delete_set', [this.$store.state.activeProject.project.id, 'packageset', packageSet.packageset.numindex]) // Go to the server to delete the package set.
          .then(response => {
            this.updatePackageSets() // Update the package sets so the new set shows up on the list.
          })
      },

      createNewPackageSet() {
        console.log('createNewPackageSet() called')
        rpcs.rpc('create_packageset', [this.$store.state.activeProject.project.id, this.burdenSet, this.intervSet]) // Go to the server to create the new package set.
          .then(response => {
            this.updatePackageSets() // Update the package sets so the new set shows up on the list.
          })
          .catch(error => {
            status.fail(this, 'Could not create new package sets', error)
          })
      },

      updateSorting2(sortColumn) {
        console.log('updateSorting2() called')
        if (this.sortColumn2 === sortColumn) { // If the active sorting column is clicked...
          this.sortReverse2 = !this.sortReverse2 // Reverse the sort.
        } else { // Otherwise.
          this.sortColumn2 = sortColumn // Select the new column for sorting.
          this.sortReverse2 = false // Set the sorting for non-reverse.
        }
      },

      applyIntervFilter(intervs) {
        return intervs.filter(theInterv => (theInterv.name.toLowerCase().indexOf(this.filterText2.toLowerCase()) !== -1) ||
        (theInterv.cause.toLowerCase().indexOf(this.filterText2.toLowerCase()) !== -1))
      },

      applySorting2(results) {
        return results.sort((result1, result2) =>
          {
            let sortDir = this.sortReverse2 ? -1: 1
            if      (this.sortColumn2 === 'name')         {return (result1[0] > result2[0] ? sortDir: -sortDir)}
            else if (this.sortColumn2 === 'cause')        {return (result1[1] > result2[1] ? sortDir: -sortDir)}
            else if (this.sortColumn2 === 'spend')     {return (result1[2] > result2[2] ? sortDir: -sortDir)}
            else if (this.sortColumn2 === 'opt_spend') {return (result1[3] > result2[3] ? sortDir: -sortDir)}
            else if (this.sortColumn2 === 'averted')      {return (result1[4] > result2[4] ? sortDir: -sortDir)}
            else if (this.sortColumn2 === 'opt_averted')  {return (result1[5] > result2[5] ? sortDir: -sortDir)}
          }
        )
      },

      updateResult(result) {
        console.log('Update to be made to results -- WARNING, not supported!')
        console.log('Index: ',   result.numindex)
        console.log('Active?: ', result.active)
        console.log('Cause: ',   result.name)
        console.log('DALYs: ',   result.cause)
      }

    }
  }
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style lang="scss" scoped>

</style>
