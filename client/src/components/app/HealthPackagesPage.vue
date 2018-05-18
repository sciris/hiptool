<!--
Define health packages

Last update: 2018-05-18
-->

<template>
  <div class="SitePage">

    <div v-if="activeProjectName === ''">
      <div style="font-style:italic">
        <p>Hmm, I can't find any health packages...did you forget to <router-link to="/projects">load a project</router-link>?</p>
      </div>
    </div>

    <div class="PageSection" v-if="activeProjectName !== ''">

      <button class="btn" @click="createNewPackageSet">Create new health benefits package</button>

      <span>&nbsp;based on [FIX]</span>

      <select
        title="countrySelect"
        id="country"
        :required="true"
        v-model="country">
        <option
          v-for = "country in countryList"
          :value="country"
        >
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
            <button class="btn __red" @click="deletePackageSet(packageSet)">Delete</button>
          </td>
        </tr>
        </tbody>
      </table>
    </div>

    <div class="PageSection UIPlaceholder" v-if="activePackageSet.packageset != undefined">

      <div>
        <div id="fig01" style="float:left" ></div>
        <div id="fig02" style="float:left" ></div>
      </div>



      <table class="table table-bordered table-hover table-striped" style="width: 100%; margin-top: 10px;">
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
        <tr v-for="disease in sortedDiseases">
          <td style="text-align: center">
            <input type="checkbox"
                   v-model="disease.active"/>
          </td>
          <td>
            <input type="text"
                   class="txbox"
                   @keyup.enter="updateDisease(disease)"
                   v-model="disease.cause"/>
          </td>
          <td>
            <input type="text"
                   class="txbox"
                   @keyup.enter="updateDisease(disease)"
                   v-model="disease.dalys"/>
          </td>
          <td>
            <input type="text"
                   class="txbox"
                   @keyup.enter="updateDisease(disease)"
                   v-model="disease.deaths"/>
          </td>
          <td>
            <input type="text"
                   class="txbox"
                   @keyup.enter="updateDisease(disease)"
                   v-model="disease.prevalence"/>
          </td>
          <td style="white-space: nowrap; text-align:center">
            <button class="iconbtn" @click="notImplemented('Copy')"><i class="ti-layers"></i></button>
            <button class="iconbtn" @click="notImplemented('Delete')"><i class="ti-trash"></i></button>
          </td>
        </tr>
        </tbody>
      </table>

      <!--<template>-->
      <!--Testing handsontable-->
      <!--<div id="hot-preview">-->
      <!--<HotTable :root="root" :settings="hotSettings"></HotTable>-->
      <!--</div>-->
      <!--</template>-->

    </div>
  </div>
</template>

<script>
  import axios from 'axios'
  var filesaver = require('file-saver')
  import rpcservice from '@/services/rpc-service'
  import router from '@/router'
  //  import HotTable from 'vue-handsontable-official';
  import Vue from 'vue';

  export default {
    name: 'HealthPackagesPage',
//    components: {
//        HotTable
//    },
    data() {
      return {
        // Placeholder text for table filter box
        filterPlaceholder: 'Type here to filter health packages',

        // Text in the table filter box
        filterText: '',

        // Column of table used for sorting the health package sets
        sortColumn: 'updatedTime',  // name, creationTime, updatedTime

        // Sort in reverse order?
        sortReverse: false,

        root: 'test-hot',
        hotSettings: {
          data: [['sample', 'data']],
          colHeaders: true
        },

        // List of health package sets in the active project
        packageSets: [],

        // Active health package set
        activePackageSet: {},

        // List of diseases.  Each list element is a list of the ailment name
        // and numbers associated with it.
        diseaseList: [],

        // Column of table used for sorting the diseases
        sortColumn2: 'name',  // name, country, creationTime, updatedTime

        // Sort diseases in reverse order?
        sortReverse2: false,

        // CK: WARNING TEMP, should come from backend
        country: 'Afghanistan',
        countryList: [
          'Afghanistan',
          'Other',
        ],

        serverresponse: 'no response',
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

      sortedDiseases() {
        var sortedDiseaseList =  this.applySorting2(this.diseaseList);
        Vue.set(this.hotSettings, 'data', [[1,2,3]]);
        console.log(sortedDiseaseList);
        return sortedDiseaseList;
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
        this.$notifications.notify({
          message: 'Function "' + message + '" not yet implemented',
          icon: 'ti-face-sad',
          type: 'warning',
          verticalAlign: 'top',
          horizontalAlign: 'center',
        });
      },

      updatePackageSets(setLastEntryActive=false) {
        console.log('updatePackageSets() called')

        // If there is no active project, clear the packageSets list.
        if (this.$store.state.activeProject.project === undefined) {
          this.packageSets = []
        }

        // Otherwise...
        else {
          // Get the active project's health package sets.
          rpcservice.rpcProjectCall('get_project_package_sets',
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
        rpcservice.rpcProjectCall('get_project_package_set_diseases',
          [this.$store.state.activeProject.project.id, this.activePackageSet.packageset.numindex])
          .then(response => {
            // Set the disease list.
            this.diseaseList = response.data.diseases

            // Set the active values from the loaded in data.
            for (let ind=0; ind < this.diseaseList.length; ind++) {
              this.diseaseList[ind].numindex = ind
              this.diseaseList[ind].active = (this.diseaseList[ind][0] > 0)
              this.diseaseList[ind].cause = this.diseaseList[ind][1]
              this.diseaseList[ind].dalys = Number(this.diseaseList[ind][2]).toLocaleString()
              this.diseaseList[ind].deaths = Number(this.diseaseList[ind][3]).toLocaleString()
              this.diseaseList[ind].prevalence = Number(this.diseaseList[ind][4]).toLocaleString()
            }

            // Reset the bottom table sorting state.
            this.sortColumn2 = 'name'
            this.sortReverse2 = false

            // Plot graphs
            this.makeGraph(packageSet)
          })

        this.$notifications.notify({
          message: 'Health package "' + packageSet.packageset.name + '" now active',
          icon: 'ti-check',
          type: 'success',
          verticalAlign: 'top',
          horizontalAlign: 'center',
        });
      },

      makeGraph(packageSet) {
        console.log('makeGraph() called for ' + packageSet.packageset.name)

        // Set the active project to the matched project.
        this.activePackageSet = packageSet

        // Go to the server to get the diseases from the package set.
        rpcservice.rpcProjectCall('get_project_package_plots',
          [this.$store.state.activeProject.project.id, this.activePackageSet.packageset.numindex])
          .then(response => {
            this.serverresponse = response.data // Pull out the response data.
            let theFig = response.data.graph1 // Extract hack info.
            mpld3.draw_figure('fig01', response.data.graph1) // Draw the figure.
            mpld3.draw_figure('fig02', response.data.graph2) // Draw the figure.
            mpld3.draw_figure('fig03', response.data.graph3) // Draw the figure.
          })
          .catch(error => {
            // Pull out the error message.
            this.serverresponse = 'There was an error: ' + error.message

            // Set the server error.
            this.servererror = error.message
          })
      },

      copyPackageSet(packageSet) {
        console.log('copyPackageSet() called for ' + packageSet.packageset.name)

        // Have the server copy the package set, giving it a new name.
        rpcservice.rpcProjectCall('copy_package_set',
          [this.$store.state.activeProject.project.id, packageSet.packageset.numindex])
          .then(response => {
            // Update the package sets so the new set shows up on the list.
            this.updatePackageSets()
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
          rpcservice.rpcProjectCall('rename_package_set',
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
        rpcservice.rpcProjectCall('delete_package_set',
          [this.$store.state.activeProject.project.id, packageSet.packageset.numindex])
          .then(response => {
            // Update the package sets so the new set shows up on the list.
            this.updatePackageSets()
          })
      },

      createNewPackageSet() {
        console.log('createNewPackageSet() called')

        // Go to the server to create the new package set.
        rpcservice.rpcProjectCall('create_package_set',
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

      applySorting2(diseases) {
        return diseases.sort((disease1, disease2) =>
          {
            let sortDir = this.sortReverse2 ? -1: 1
            if (this.sortColumn2 === 'name') {
              return (disease1[1] > disease2[1] ? sortDir: -sortDir)
            }
            else if (this.sortColumn2 === 'DALYs') {
              return disease1[2] > disease2[2] ? sortDir: -sortDir
            }
            else if (this.sortColumn2 === 'deaths') {
              return disease1[3] > disease2[3] ? sortDir: -sortDir
            }
            else if (this.sortColumn2 === 'prevalence') {
              return disease1[4] > disease2[4] ? sortDir: -sortDir
            }
          }
        )
      },

      updateDisease(disease) {
        console.log('Update to be made')
        console.log('Index: ', disease.numindex)
        console.log('Active?: ', disease.active)
        console.log('Cause: ', disease.cause)
        console.log('DALYs: ', disease.dalys)
        console.log('Deaths: ', disease.deaths)
        console.log('Prevalence: ', disease.prevalence)

        // Do format filtering to prepare the data to pass to the RPC.
        let filterActive = disease.active ? 1 : 0

        // Go to the server to update the disease from the package set.
        // Note: filter out commas in the numeric fields.
        rpcservice.rpcProjectCall('update_package_set_disease',
          [this.$store.state.activeProject.project.id,
            this.activePackageSet.packageset.numindex,
            disease.numindex,
            [filterActive, disease.cause,
              disease.dalys.replace(/,/g, ''),
              disease.deaths.replace(/,/g, ''),
              disease.prevalence.replace(/,/g, '')]])
          .then(response => {
            // Update the display of the disease list by rerunning the active
            // package set.
            this.viewPackageSet(this.activePackageSet)
          })
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
