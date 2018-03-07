<!--
DiseaseBurdenPage.vue -- DiseaseBurdenPage Vue component

Last update: 3/7/18 (gchadder3)
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
              Burden project
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
            <th>Country</th>
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
          <tr v-for="projectSummary in sortedFilteredProjectSummaries" :class="{ highlighted: activeProject.uid === projectSummary.uid }">
            <td>{{ projectSummary.projectName }}</td>
            <td>{{ projectSummary.country }}</td>
            <td>{{ projectSummary.creationTime }}</td>
            <td>{{ projectSummary.updateTime ? projectSummary.updateTime:
              'No modification' }}</td>
            <td style="white-space: nowrap">
              <button class="btn __green" @click="viewProject(projectSummary.uid)">View</button>
              <button class="btn" @click="copyProject(projectSummary.uid)">Copy</button>
              <button class="btn" @click="renameProject(projectSummary.uid)">Rename</button>
              <button class="btn __red" @click="deleteProject(projectSummary.uid)">Delete</button>
            </td>
          </tr>
          <tr>
            <td>
              <button class="btn" @click="createNewProject">Create new</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <div class="PageSection UIPlaceholder" v-if="activeProject.projectName != undefined">
      <div class="PHText">
        Page interface specific to {{ activeProject.projectName }} project
      </div>

      <button class="btn" @click="grabTableData">Upload IHME data</button>

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

export default {
  name: 'DiseaseBurdenPage',

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

      // List of summary objects for projects the user has
      projectSummaries:
        [
          {
            projectName: 'Default GBD',
            country: 'Afghanistan',
            creationTime: '2017-Jun-01 02:45 AM',
            updateTime: '2017-Jun-02 05:41 AM',
            uid: 1
          },
          {
            projectName: 'GBD with updated NCDs',
            country: 'Afghanistan',
            creationTime: '2017-Jun-07 05:15 PM',
            updateTime: '2017-Jun-08 05:14 PM',
            uid: 2
          }
        ],

      // Active project
      activeProject: {},

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
    sortedFilteredProjectSummaries() {
      return this.applyNameFilter(this.applySorting(this.projectSummaries))
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

    applyNameFilter(projects) {
      console.log('applyNameFilter() called')

      return projects.filter(theProject => theProject.projectName.toLowerCase().indexOf(this.filterText.toLowerCase()) !== -1)
    },

    applySorting(projects) {
      console.log('applySorting() called')

      return projects.sort((proj1, proj2) =>
        {
          let sortDir = this.sortReverse ? -1: 1
          if (this.sortColumn === 'name') {
            return (proj1.projectName > proj2.projectName ? sortDir: -sortDir)
          }
          else if (this.sortColumn === 'country') {
            return proj1.country > proj2.country ? sortDir: -sortDir
          }
          else if (this.sortColumn === 'creationTime') {
            return proj1.creationTime > proj2.creationTime ? sortDir: -sortDir
          }
          else if (this.sortColumn === 'updatedTime') {
            return proj1.updateTime > proj2.updateTime ? sortDir: -sortDir
          }
        }
      )
    },

    viewProject(uid) {
      // Find the project that matches the UID passed in.
      let matchProject = this.projectSummaries.find(theProj => theProj.uid === uid)

      console.log('viewProject() called for ' + matchProject.projectName)

      // Set the active project to the matched project.
      this.activeProject = matchProject

      // Clear the disease list (for now) and reset the bottom table sorting state.
      this.diseaseList = []
      this.sortColumn2 = 'name'
      this.sortReverse2 = false
    },

    copyProject(uid) {
      // Find the project that matches the UID passed in.
      let matchProject = this.projectSummaries.find(theProj => theProj.uid === uid)

      console.log('copyProject() called for ' + matchProject.projectName)
    },

    renameProject(uid) {
      // Find the project that matches the UID passed in.
      let matchProject = this.projectSummaries.find(theProj => theProj.uid === uid)

      console.log('renameProject() called for ' + matchProject.projectName)
    },

    deleteProject(uid) {
      // Find the project that matches the UID passed in.
      let matchProject = this.projectSummaries.find(theProj => theProj.uid === uid)

      console.log('deleteProject() called for ' + matchProject.projectName)
    },

    createNewProject() {
      console.log('createNewProject() called')
    },

    grabTableData() {
      console.log('grabTableData() called')
      rpcservice.rpcCall('read_ihme_table')
      .then(response => {
        this.diseaseList = response.data.diseases
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
      console.log('applySorting2() called')

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
</style>
