<!--
Define health packages

Last update: 2018-05-29
-->

<template>
  <div class="SitePage">

    <div v-if="activeProjectName === ''">
      <div style="font-style:italic">
        <p>Hmm, I can't find any health packages...did you forget to <router-link to="/projects">load a project</router-link>?</p>
      </div>
    </div>

    <div class="PageSection" v-if="activeProjectName !== ''">


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
      <button v-show="!showingPlots" class="btn" @click="showPlots">Show plots</button>
      <button v-show="showingPlots" class="btn" @click="hidePlots">Hide plots</button>
      <button class="btn" @click="downloadPlots">Download plots</button>
    </div>

    <div class="PageSection UIPlaceholder" v-if="activePackageSet.packageset != undefined">

      <div v-show="showingPlots">
        <div id="fig1" style="float:left" ></div>
        <div id="fig2" style="float:left" ></div>
        <div id="fig3" style="float:left" ></div>
      </div>


      <table class="table table-bordered table-hover table-striped" style="width: 100%; margin-top: 10px;">
        <thead>
        <tr>
          <th style="text-align:center">Active</th>
          <th @click="updateSorting2('name')" class="sortable">Intervention
            <span v-show="sortColumn2 == 'name' && !sortReverse2"><i class="fas fa-caret-down"></i></span>
            <span v-show="sortColumn2 == 'name' && sortReverse2"><i class="fas fa-caret-up"></i></span>
            <span v-show="sortColumn2 != 'name'"><i class="fas fa-caret-up" style="visibility: hidden"></i></span>
          </th>
          <th @click="updateSorting2('cause')" class="sortable">Cause of burden
            <span v-show="sortColumn2 == 'cause' && !sortReverse2"><i class="fas fa-caret-down"></i></span>
            <span v-show="sortColumn2 == 'cause' && sortReverse2"><i class="fas fa-caret-up"></i></span>
            <span v-show="sortColumn2 != 'cause'"><i class="fas fa-caret-up" style="visibility: hidden"></i></span>
          </th>
          <th @click="updateSorting2('coverage')" class="sortable">Number of people covered
            <span v-show="sortColumn2 == 'coverage' && !sortReverse2"><i class="fas fa-caret-down"></i></span>
            <span v-show="sortColumn2 == 'coverage' && sortReverse2"><i class="fas fa-caret-up"></i></span>
            <span v-show="sortColumn2 != 'coverage'"><i class="fas fa-caret-up" style="visibility: hidden"></i></span>
          </th>
          <th @click="updateSorting2('averted')" class="sortable">DALYs averted (per year)
            <span v-show="sortColumn2 == 'averted' && !sortReverse2"><i class="fas fa-caret-down"></i></span>
            <span v-show="sortColumn2 == 'averted' && sortReverse2"><i class="fas fa-caret-up"></i></span>
            <span v-show="sortColumn2 != 'averted'"><i class="fas fa-caret-up" style="visibility: hidden"></i></span>
          </th>
          <th @click="updateSorting2('percentage')" class="sortable">DALYs averted (%)
            <span v-show="sortColumn2 == 'percentage' && !sortReverse2"><i class="fas fa-caret-down"></i></span>
            <span v-show="sortColumn2 == 'percentage' && sortReverse2"><i class="fas fa-caret-up"></i></span>
            <span v-show="sortColumn2 != 'percentage'"><i class="fas fa-caret-up" style="visibility: hidden"></i></span>
          </th>
        </tr>
        </thead>
        <tbody>
        <tr v-for="result in sortedResults">
          <td style="text-align: center">
            <input type="checkbox"
                   v-model="result.active"/>
          </td>
          <td>
            {{ result.name }}
          </td>
          <td>
            {{ result.cause }}
          </td>
          <td>
            {{ result.coverage }}
          </td>
          <td>
            {{ result.averted }}
          </td>
          <td>
            {{ result.percentage }}
          </td>
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
        filterPlaceholder: 'Type here to filter health packages', // Placeholder text for table filter box
        filterText: '', // Text in the table filter box
        sortColumn: 'updatedTime',  // Column of table used for sorting the health package sets // name, creationTime, updatedTime
        sortReverse: false, // Sort in reverse order?
        packageSets: [], // List of health package sets in the active project
        activePackageSet: {}, // Active health package set
        resultList: [], // List of diseases.  Each list element is a list of the ailment name and numbers associated with it.
        sortColumn2: 'name',  // Column of table used for sorting the diseases // name, country, creationTime, updatedTime
        sortReverse2: true, // Sort diseases in reverse order?
        serverresponse: 'no response',
        showingPlots: false,
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

      sortedResults() {
        var sortedResultList =  this.applySorting2(this.resultList);
        console.log(sortedResultList);
        return sortedResultList;
      },

    },

    created() {
      // If we have no user logged in, automatically redirect to the login page.
      if (this.$store.state.currentUser.displayname == undefined) {
        router.push('/login')
      }

      // Otherwise...
      else {
        // Load the health package sets from the active project, telling the function
        // to also set the active health package set to the last item.
        this.updatePackageSets(true)
      }
    },

    methods: {

      notImplemented(message) {
        status.fail(this, 'Function "' + message + '" not yet implemented')
      },

      clearGraphs(numfigs) { return utils.clearGraphs(this, numfigs)},

      showPlots() {
        this.showingPlots = true
      },

      hidePlots() {
        this.showingPlots = false
      },

      downloadPlots() {
        rpcs.download('download_figures', [])
          .then(response => {
            console.log('Downloaded figures')
          })
      },

      updatePackageSets(setLastEntryActive) {
        console.log('updatePackageSets() called')

        // If there is no active project, clear the packageSets list.
        if (this.$store.state.activeProject.project === undefined) {
          this.packageSets = []
        }

        // Otherwise...
        else {
          // Get the active project's health package sets.
          rpcs.rpc('get_project_package_sets',
            [this.$store.state.activeProject.project.id])
            .then(response => {
              // Set the package set list to what we received.
              this.packageSets = response.data.packagesets

              // Add numindex elements to the package sets to keep track of
              // which index to pull from the server.
              for (let ind=0; ind < this.packageSets.length; ind++)
                this.packageSets[ind].packageset.numindex = ind

              // Set renaming values to blank initially.
              this.packageSets.forEach(theSet => {
                theSet.renaming = ''
              })

              // If we want to set the last entry active and we have any
              // entries, do the setting.
              if ((setLastEntryActive) && (this.packageSets.length > 0))
                this.viewPackageSet(this.packageSets[this.packageSets.length - 1])
            })
            .catch(error => {
              status.fail(this, 'Could not get package sets', error)
            })
        }
      },

      packageSetIsSelected(packageSet) {
        // If the active package set is undefined, it is not active.
        if (this.activePackageSet.packageset === undefined) {
          return false
        }

        // Otherwise, the package set is selected if the numindexes match.
        else {
          return (this.activePackageSet.packageset.numindex === packageSet.packageset.numindex)
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

        // Set the active project to the packageSet passed in.
        this.activePackageSet = packageSet

        // Go to the server to get the diseases from the package set.
        rpcs.rpc('get_project_package_set_results',
          [this.$store.state.activeProject.project.id, this.activePackageSet.packageset.numindex])
          .then(response => {
            // Set the result list.
            this.resultList = response.data.results

            // Set the active values from the loaded in data.
            for (let ind=0; ind < this.resultList.length; ind++) {
              this.resultList[ind].numindex = ind
              this.resultList[ind].active = (this.resultList[ind][0] > 0)
              this.resultList[ind].name = this.resultList[ind][1]
              this.resultList[ind].cause = this.resultList[ind][2]
              this.resultList[ind].coverage = Math.round(Number(this.resultList[ind][3])).toLocaleString()
              this.resultList[ind].averted = Math.round(Number(this.resultList[ind][4])).toLocaleString()
              this.resultList[ind].percentage = (Number(this.resultList[ind][5])*100).toLocaleString() // Convert to percentage
            }

            // Reset the bottom table sorting state.
            this.sortColumn2 = 'name'
            this.sortReverse2 = false

            // Plot graphs
            this.makeGraph(packageSet)
          })
          .catch(error => {
            status.fail(this, 'Could not view health package sets', error)
          })

        status.succeed(this, 'Health package "' + packageSet.packageset.name + '" now active')
      },

      makeGraph(packageSet) {
        console.log('makeGraph() called for ' + packageSet.packageset.name)

        // Set the active project to the matched project.
        this.activePackageSet = packageSet
        this.clearGraphs(3)

        // Go to the server to get the results from the package set.
        rpcs.rpc('get_project_package_plots',
          [this.$store.state.activeProject.project.id, this.activePackageSet.packageset.numindex])
          .then(response => {
            this.serverresponse = response.data // Pull out the response data.
            let theFig = response.data.graph1 // Extract hack info.
            mpld3.draw_figure('fig1', response.data.graph1) // Draw the figure.
            mpld3.draw_figure('fig2', response.data.graph2) // Draw the figure.
            mpld3.draw_figure('fig3', response.data.graph3) // Draw the figure.
          })
          .catch(error => {
            status.fail(this, 'Could not make graphs', error)
          })
      },

      copyPackageSet(packageSet) {
        console.log('copyPackageSet() called for ' + packageSet.packageset.name)

        // Have the server copy the package set, giving it a new name.
        rpcs.rpc('copy_package_set',
          [this.$store.state.activeProject.project.id, packageSet.packageset.numindex])
          .then(response => {
            // Update the package sets so the new set shows up on the list.
            this.updatePackageSets()
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

        // If the package set is not in a mode to be renamed, make it so.
        if (packageSet.renaming === '') {
          packageSet.renaming = packageSet.packageset.name
        }

        // Otherwise (it is to be renamed)...
        else {
          // Have the server change the name of the package set.
          rpcs.rpc('rename_package_set',
            [this.$store.state.activeProject.project.id,
              packageSet.packageset.numindex, packageSet.renaming])
            .then(response => {
              // Update the package sets so the renamed one shows up on the list.
              this.updatePackageSets()

              // Turn off the renaming mode.
              packageSet.renaming = ''
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

        // Go to the server to delete the package set.
        rpcs.rpc('delete_package_set',
          [this.$store.state.activeProject.project.id, packageSet.packageset.numindex])
          .then(response => {
            // Update the package sets so the new set shows up on the list.
            this.updatePackageSets()
          })
      },

      createNewPackageSet() {
        console.log('createNewPackageSet() called')

        // Go to the server to create the new package set.
        rpcs.rpc('create_package_set',
          [this.$store.state.activeProject.project.id, 'New package set'])
          .then(response => {
            // Update the package sets so the new set shows up on the list.
            this.updatePackageSets()
          })
      },


      updateSorting2(sortColumn) {
        console.log('updateSorting2() called')

        // If the active sorting column is clicked...
        if (this.sortColumn2 === sortColumn) {
          // Reverse the sort.
          this.sortReverse2 = !this.sortReverse2
        }
        // Otherwise.
        else {
          // Select the new column for sorting.
          this.sortColumn2 = sortColumn

          // Set the sorting for non-reverse.
          this.sortReverse2 = false
        }
      },

      applySorting2(results) {
        return results.sort((result1, result2) =>
          {
            let sortDir = this.sortReverse2 ? -1: 1
            if      (this.sortColumn2 === 'name') {return (result1[1] > result2[1] ? sortDir: -sortDir)}
            else if (this.sortColumn2 === 'cause') {return result1[2] > result2[2] ? sortDir: -sortDir}
            else if (this.sortColumn2 === 'coverage') {return result1[3] > result2[3] ? sortDir: -sortDir}
            else if (this.sortColumn2 === 'averted') {return result1[4] > result2[4] ? sortDir: -sortDir}
            else if (this.sortColumn2 === 'percentage') {return result1[5] > result2[5] ? sortDir: -sortDir}
          }
        )
      },

      updateResult(result) {
        console.log('Update to be made to results -- WARNING, not supported!')
        console.log('Index: ', result.numindex)
        console.log('Active?: ', result.active)
        console.log('Cause: ', result.name)
        console.log('DALYs: ', result.cause)
      }

    }
  }
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style lang="scss" scoped>
  .UIPlaceholder {
    width: 100%;
  }

  .PHText {
    color: green;
    text-align: center;
  }

  .ThreePanels {
    display: flex;
    width: 100%;
  }

  .LeftPanel {
    height: 100%;
    width: 33%;
    text-align: center;
  }

  .MidPanel {
    height: 100%;
    width: 34%;
    text-align: center;
  }

  .RightPanel {
    height: 100%;
    width: 33%;
    text-align: center;
  }

  #test-hot {
    width: 600px;
    height: 400px;
    overflow: hidden;
  }
</style>
