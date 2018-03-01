<!--
DiseaseBurdenPage.vue -- DiseaseBurdenPage Vue component

Last update: 2/28/18 (gchadder3)
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

      <button @click="grabTableData">Push the pretty button</button>

<!-- Cliff inserted this...
      <div class="PageSection UIPlaceholder">
        <div class="PHText">
          Page interface specific to {{ activeIntervSet.setName }} burden set
        </div>

        <div style="margin-top: 10px">
          <table id="checkboxtable" class="table table-bordered" style="width: auto">
            <tr>
              <td>
                Categories of burden
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
              <th>Include</th>
              <th>Cause name</th>
              <th>DALYs</th>
              <th>Deaths</th>
              <th>Prevalence</th>
              <th>Actions</th>
            </tr>
            </thead>
            <tbody>
            <tr v-for="interv in filteredInterventions">
              <td style="text-align: center">
                <input type="checkbox" v-model="interv.included"/>
              </td>
              <td>{{ interv.interventionName }}</td>
              <td>
                <input type="text" />
              </td>
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
                <button class="btn">Add new cause</button>
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
        </div>
      </div>
end of Cliff insert -->


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
      activeIntervSet: 1,

      // Show all of the intervention categories
      showAllIntervs: true,

      // Show cancer interventions
      showCancerIntervs: false,

      // Show infectious diseases interventions
      showInfectiousIntervs: false,

      // Show child care interventions
      showChildIntervs: false,

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
        ]
    }
  },

  computed: {
    sortedFilteredProjectSummaries() {
      return this.applyNameFilter(this.applySorting(this.projectSummaries))
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
