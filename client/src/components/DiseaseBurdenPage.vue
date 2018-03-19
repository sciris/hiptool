<!--
DiseaseBurdenPage.vue -- DiseaseBurdenPage Vue component

Last update: 3/14/18 (gchadder3)
-->

<template>
  <div class="SitePage">
    <h2>Open Project: {{ activeProjectName }}</h2>

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
<!--            <th>Country</th> -->
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
              :class="{ highlighted: burdenSetIsSelected(burdenSet.burdenset.uid) }">
            <td>{{ burdenSet.burdenset.name }}</td>
<!--            <td>{{ burdenSet.country }}</td> -->
            <td>{{ burdenSet.burdenset.creationTime }}</td>
            <td>{{ burdenSet.burdenset.updateTime ? burdenSet.burdenset.updateTime:
              'No modification' }}</td>
            <td style="white-space: nowrap">
              <button class="btn __green" @click="viewBurdenSet(burdenSet.burdenset.uid)">View</button>
              <button class="btn" @click="copyBurdenSet(burdenSet.burdenset.uid)">Copy</button>
              <button class="btn" @click="renameBurdenSet(burdenSet.burdenset.uid)">Rename</button>
              <button class="btn __red" @click="deleteBurdenSet(burdenSet.burdenset.uid)">Delete</button>
            </td>
          </tr>
          <tr>
            <td>
              <button class="btn" @click="createNewBurdenSet">Create new</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <div class="PageSection UIPlaceholder" v-if="activeBurdenSet.burdenset != undefined">
<!--      <div class="PHText">
        Page interface specific to {{ activeBurdenSet.burdenset.name }} project
      </div> -->

      <button class="btn" @click="grabTableData">Upload IHME data</button>

      <button class="btn" @click="makeGraph(activeBurdenSet.burdenset.uid)">Visualize</button>

      <div>
        <div id="fig01" style="float:left" ></div>
        <div id="fig02" style="float:left" ></div>
        <div id="fig03" style="float:left" ></div>
      </div>

      <template>
        <div id="hot-preview">
          <HotTable :root="root" :settings="hotSettings"></HotTable>
        </div>
      </template>


      <table class="table table-bordered table-hover table-striped" style="width: auto; margin-top: 10px;">
        <thead>
          <tr>
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
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="disease in sortedDiseases">
            <td>{{ disease[0] }}</td>
            <td>{{ disease[1] }}</td>
            <td>{{ disease[2] }}</td>
            <td>{{ disease[3] }}</td>
            <td style="white-space: nowrap">
              <button class="btn">Rename</button>
              <button class="btn __red">Delete</button>
            </td>
          </tr>
          <tr>
            <td>
              <button class="btn">Create new</button>
            </td>
          </tr>
        </tbody>
      </table>


<!-- old ThreePanels stuff
      <div class="ThreePanels">
        <div class="LeftPanel">
          <div style="margin-top: 10px">
            <img src="../assets/images/bod_img1.png" width="350"/>
          </div>
          <div style="margin-top: 10px">
            <button class="btn">Edit</button>
            <button class="btn">Download data</button>
          </div>
        </div>
        <div class="MidPanel">
          <div style="margin-top: 10px">
            <img src="../assets/images/bod_img2.png" width="350"/>
          </div>
          <div style="margin-top: 10px">
            <button class="btn">Edit</button>
            <button class="btn">Download data</button>
          </div>
        </div>
        <div class="RightPanel">
          <div style="margin-top: 10px">
            <img src="../assets/images/bod_img3.png" width="350"/>
          </div>
          <div style="margin-top: 10px">
            <button class="btn">Edit</button>
            <button class="btn">Download data</button>
          </div>
        </div>
      </div>
end of ThreePanels stuff -->

    </div>
  </div>
</template>

<script>
import axios from 'axios'
var filesaver = require('file-saver')
import rpcservice from '../services/rpc-service'
import router from '../router'
import HotTable from 'vue-handsontable-official';


export default {
  name: 'DiseaseBurdenPage',
  components: {
      HotTable
  }, 
  data() {
    return {
      // Placeholder text for table filter box
      filterPlaceholder: '\u{1f50e} Filter Burden Projects',

      // Text in the table filter box
      filterText: '',

      // Column of table used for sorting the projects
      sortColumn: 'name',  // name, country, creationTime, updatedTime

      // Sort in reverse order?
      sortReverse: false,

      root: 'test-hot',
      hotSettings: {
        data: [['sample', 'data']],
        colHeaders: true
      },
      
    


/* old burden sets stuff to get rid of
      // List of burden sets in the active project
      burdenSets:
        [
          {
            name: 'Default GBD',
//            country: 'Afghanistan',
            creationTime: '2017-Jun-01 02:45 AM',
            updateTime: '2017-Jun-02 05:41 AM',
            uid: 1
          },
          {
            name: 'GBD with updated NCDs',
//            country: 'Afghanistan',
            creationTime: '2017-Jun-07 05:15 PM',
            updateTime: '2017-Jun-08 05:14 PM',
            uid: 2
          }
        ], */

      // List of burden sets in the active project
      burdenSets: [],

      // Active burden set
      activeBurdenSet: {},

      // List of diseases.  Each list element is a list of the ailment name
      // and numbers associated with it.
      diseaseList: [],

      // Column of table used for sorting the diseases
      sortColumn2: 'name',  // name, country, creationTime, updatedTime

      // Sort diseases in reverse order?
      sortReverse2: false
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

    sortedFilteredBurdenSets() {
      return this.applyNameFilter(this.applySorting(this.burdenSets))
    },

    sortedDiseases() {
      return this.applySorting2(this.diseaseList)
    }
  },

  created() {
    // If we have no user logged in, automatically redirect to the login page.
    if (this.$store.state.currentUser.displayname == undefined) {
      router.push('/login')
    }

    // Otherwise...
    else {
      // Load the burden sets from the active project.
      this.updateBurdenSets()
    }
  },

  methods: {
    updateBurdenSets() {
      console.log('updateBurdenSets() called')

      // If there is no active project, clear the burdenSets list.
      if (this.$store.state.activeProject.project === undefined) {
        this.burdenSets = []
      }

      // Otherwise...
      else {
        // Get the active project's burden sets.
        rpcservice.rpcProjectCall('get_project_burden_sets',
          [this.$store.state.activeProject.project.id])
        .then(response => {
          // Set the burden set list to what we received.
          this.burdenSets = response.data.burdensets
        })
      }
    },

    burdenSetIsSelected(uid) {
      // If the active burden set is undefined, it is not active.
      if (this.activeBurdenSet.burdenset === undefined) {
        return false
      }

      // Otherwise, the burden set is selected if the UIDs match.
      else {
        return (this.activeBurdenSet.burdenset.uid === uid)
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
      return sets.filter(theSet => theSet.burdenset.name.toLowerCase().indexOf(this.filterText.toLowerCase()) !== -1)
    },

    applySorting(sets) {
      return sets.sort((set1, set2) =>
        {
          let sortDir = this.sortReverse ? -1: 1
          if (this.sortColumn === 'name') {
            return (set1.burdenset.name > set2.burdenset.name ? sortDir: -sortDir)
          }
/*          else if (this.sortColumn === 'country') {
            return set1.burdenset.country > set2.burdenset.country ? sortDir: -sortDir
          } */
          else if (this.sortColumn === 'creationTime') {
            return set1.burdenset.creationTime > set2.burdenset.creationTime ? sortDir: -sortDir
          }
          else if (this.sortColumn === 'updatedTime') {
            return set1.burdenset.updateTime > set2.burdenset.updateTime ? sortDir: -sortDir
          }
        }
      )
    },

    viewBurdenSet(uid) {
      // Find the burden set that matches the UID passed in.
      let matchSet = this.burdenSets.find(theSet => theSet.burdenset.uid === uid)

      console.log('viewBurdenSet() called for ' + matchSet.burdenset.name)

      // Set the active project to the matched project.
      this.activeBurdenSet = matchSet

      // Go to the server to get the diseases from the burden set.
      rpcservice.rpcProjectCall('get_project_burden_set_diseases',
        [this.$store.state.activeProject.project.id, this.activeBurdenSet.burdenset.uid])
      .then(response => {
        // Set the disease list.
        this.diseaseList = response.data.diseases

        // Reset the bottom table sorting state.
        this.sortColumn2 = 'name'
        this.sortReverse2 = false
      })
    },

    copyBurdenSet(uid) {
      // Find the burden set that matches the UID passed in.
      let matchSet = this.burdenSets.find(theSet => theSet.burdenset.uid === uid)

      console.log('copyBurdenSet() called for ' + matchSet.burdenset.name)
    },

    renameBurdenSet(uid) {
      // Find the burden set that matches the UID passed in.
      let matchSet = this.burdenSets.find(theSet => theSet.burdenset.uid === uid)

      console.log('renameBurdenSet() called for ' + matchSet.burdenset.name)
    },

    deleteBurdenSet(uid) {
      // Find the burden set that matches the UID passed in.
      let matchSet = this.burdenSets.find(theSet => theSet.burdenset.uid === uid)

      console.log('deleteBurdenSet() called for ' + matchSet.burdenset.name)
    },

    createNewBurdenSet() {
      console.log('createNewBurdenSet() called')
    },

    grabTableData() {
      console.log('grabTableData() called')
/*      rpcservice.rpcProjectCall('get_project_burden_set_diseases',
        [this.$store.state.activeProject.project.id, this.activeBurdenSet.burdenset.uid])
      .then(response => {
        this.diseaseList = response.data.diseases
      }) */
    },

    makeGraph(uid) {
      // Find the burden set that matches the UID passed in.
      let matchSet = this.burdenSets.find(theSet => theSet.burdenset.uid === uid)

      console.log('makeGraph() called for ' + matchSet.burdenset.name)

      // Set the active project to the matched project.
      this.activeBurdenSet = matchSet

      // Go to the server to get the diseases from the burden set.
      rpcservice.rpcProjectCall('get_project_burden_plots',
        [this.$store.state.activeProject.project.id, this.activeBurdenSet.burdenset.uid])
        .then(response => {
          // Pull out the response data.
          this.serverresponse = response.data

          // Draw the figure in the 'fig01' div tag.
          mpld3.draw_figure('fig01', response.data.graph1)
          mpld3.draw_figure('fig02', response.data.graph2)
          mpld3.draw_figure('fig03', response.data.graph3)
        })
        .catch(error => {
          // Pull out the error message.
          this.serverresponse = 'There was an error: ' + error.message

          // Set the server error.
          this.servererror = error.message
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
            return (disease1[0] > disease2[0] ? sortDir: -sortDir)
          }
          else if (this.sortColumn2 === 'DALYs') {
            return disease1[1] > disease2[1] ? sortDir: -sortDir
          }
          else if (this.sortColumn2 === 'deaths') {
            return disease1[2] > disease2[2] ? sortDir: -sortDir
          }
          else if (this.sortColumn2 === 'prevalence') {
            return disease1[3] > disease2[3] ? sortDir: -sortDir
          }
        }
      )
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
//    border: 1px solid black;
  }

  .ThreePanels {
    display: flex;
//    height: 480px;
    width: 100%;
//    border: 1px solid black;
  }

  .LeftPanel {
    height: 100%;
    width: 33%;
    text-align: center;
//    border: 1px solid black;
  }

  .MidPanel {
    height: 100%;
    width: 34%;
    text-align: center;
//    border: 1px solid black;
  }

  .RightPanel {
    height: 100%;
    width: 33%;
    text-align: center;
//    border: 1px solid black;
  }
  #test-hot {
    width: 600px;
    height: 400px;
    overflow: hidden;
  }
</style>
