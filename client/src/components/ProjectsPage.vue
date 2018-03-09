<!-- 
ProjectsPage.vue -- ProjectsPage Vue component

Last update: 3/8/18 (gchadder3)
-->

<template>
  <div class="SitePage">
    <div class="PageSection">
      <h2>Create projects</h2>

      <div class="ControlsRowLabel">
        Choose a demonstration project from our database:
      </div>

      <div class="ControlsRow">
        <select v-model="selectedDemoProject">
          <option v-for="choice in demoProjectList">
            {{ choice }}
          </option>
        </select>
        &nbsp; &nbsp;
        <button class="btn" @click="addDemoProject">Add this project</button>
      </div>

      <div class="ControlsRowLabel">
        Or create/upload a new project:
      </div>

      <div class="ControlsRow">
        <button class="btn" @click="createNewProject">Create new project</button>
        &nbsp; &nbsp;
        <button class="btn" @click="uploadProjectFromFile">Upload project from file</button>
        &nbsp; &nbsp;
        <button class="btn" @click="uploadProjectFromSpreadsheet">Upload project from spreadsheet</button>
      </div>
    </div>

    <div class="PageSection"
         v-if="projectSummaries.length > 0">
      <h2>Manage projects</h2>

      <input type="text" 
             class="txbox" 
             style="margin-bottom: 20px" 
             :placeholder="filterPlaceholder"
             v-model="filterText"/>

      <table class="table table-bordered table-hover table-striped" style="width: auto">
        <thead>
          <tr>
            <th>
              <input type="checkbox" @click="selectAll()" v-model="allSelected"/>
            </th>
            <th @click="updateSorting('name')" class="sortable">
              Name
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
            <th>Select</th>
 <!--           <th @click="updateSorting('country')" class="sortable">
              Country
              <span v-show="sortColumn == 'country' && !sortReverse">
                <i class="fas fa-caret-down"></i>
              </span>
              <span v-show="sortColumn == 'country' && sortReverse">
                <i class="fas fa-caret-up"></i>
              </span>
              <span v-show="sortColumn != 'country'">
                <i class="fas fa-caret-up" style="visibility: hidden"></i>
              </span>
            </th> -->
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
            <th @click="updateSorting('dataUploadTime')" class="sortable">
              Data uploaded on
              <span v-show="sortColumn == 'dataUploadTime' && !sortReverse">
                <i class="fas fa-caret-down"></i>
              </span>
              <span v-show="sortColumn == 'dataUploadTime' && sortReverse">
                <i class="fas fa-caret-up"></i>
              </span>
              <span v-show="sortColumn != 'dataUploadTime'">
                <i class="fas fa-caret-up" style="visibility: hidden"></i>
              </span>
            </th>
            <th>Actions</th>
            <th>Data spreadsheet</th>
            <th>Project file</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="projectSummary in sortedFilteredProjectSummaries" 
              :class="{ highlighted: projectIsActive(projectSummary.project.id) }">
            <td>
              <input type="checkbox" @click="uncheckSelectAll()" v-model="projectSummary.selected"/>
            </td>
            <td>{{ projectSummary.project.name }}</td>
            <td>
              <button class="btn __green" @click="openProject(projectSummary.project.id)">Open</button>
            </td>
<!--            <td>{{ projectSummary.country }}</td> -->
            <td>{{ projectSummary.project.creationTime }}</td>
            <td>{{ projectSummary.project.updatedTime ? projectSummary.project.updatedTime: 
              'No modification' }}</td>
            <td>{{ projectSummary.project.dataUploadTime ?  projectSummary.project.dataUploadTime: 
              'No data uploaded' }}</td>
            <td style="white-space: nowrap">
              <button class="btn" @click="copyProject(projectSummary.project.id)">Copy</button>
              <button class="btn" @click="renameProject(projectSummary.project.id)">Rename</button>
            </td>
            <td style="white-space: nowrap">
              <button class="btn" @click="uploadSpreadsheetToProject(projectSummary.project.id)">Upload</button>
              <button class="btn" @click="downloadSpreadsheetFromProject(projectSummary.project.id)">Download</button>
            </td>
            <td style="white-space: nowrap">
              <button class="btn" @click="downloadProjectFile(projectSummary.project.id)">Download</button>
              <button class="btn" @click="downloadProjectFileWithResults(projectSummary.project.id)">Download with results</button>
            </td>
          </tr>
<!--          <tr>
            <td>
              <button class="btn" @click="createNewProject">Create new project</button>
            </td>
<!-- comment out for now            <td>
              <select v-model="selectedCountry">
                <option>Select country...</option>
                <option v-for="choice in countryList">
                  {{ choice }}
                </option>
              </select>
            </td> 
          </tr> -->
        </tbody>
      </table>

      <div class="ControlsRow">
        <button class="btn" @click="deleteSelectedProjects">Delete selected</button>
        &nbsp; &nbsp;
        <button class="btn" @click="downloadSelectedProjects">Download selected</button>
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
  name: 'ProjectsPage',

  data() {
    return {
      // List of projects to choose from (by project name)
      demoProjectList: [],

      // Selected demo project (by name)
      selectedDemoProject: '',

      // List of demo project summaries
      demoProjectSummaries: [],

      // Placeholder text for table filter box
      filterPlaceholder: '\u{1f50e} Filter Projects',

      // Text in the table filter box
      filterText: '',

      // Are all of the projects selected?
      allSelected: false, 

      // Column of table used for sorting the projects
      sortColumn: 'name',  // name, country, creationTime, updatedTime, dataUploadTime

      // Sort in reverse order?
      sortReverse: false, 

/* old project summaries stuff to get rid of
        // List of summary objects for projects the user has
        projectSummaries: 
        [
          {
            projectName: 'Afghanistan test 1',
            country: 'Afghanistan', 
            creationTime: '2017-Jun-01 02:45 AM',
            updateTime: '2017-Jun-02 05:41 AM',
            uid: 1
          }, 
          {
            projectName: 'Afghanistan HBP equity',
            country: 'Afghanistan', 
            creationTime: '2017-Jun-03 03:12 PM',
            updateTime: '2017-Jun-05 03:38 PM',
            uid: 2
          },
          {
            projectName: 'Final Afghanistan HBP', 
            country: 'Afghanistan', 
            creationTime: '2017-Jun-06 08:15 PM',
            updateTime: '2017-Jun-06 08:20 PM',
            uid: 3
          },
          {
            projectName: 'Pakistan test 1',
            country: 'Pakistan', 
            creationTime: '2017-Sep-21 08:44 AM',
            updateTime: '2017-Sep-21 08:44 AM',
            uid: 4
          }
        ], */

      // List of summary objects for projects the user has
      projectSummaries: [],

      // Available countries
      countryList: [],

      // Country selected in the bottom select box
      selectedCountry: 'Select country'
    }
  },

  computed: {
    sortedFilteredProjectSummaries() {
      return this.applyNameFilter(this.applySorting(this.projectSummaries))
//      return this.applyNameFilter(this.applySorting(this.applyCountryFilter(this.projectSummaries)))
    }
  }, 

  created() {
    // If we have no user logged in, automatically redirect to the login page.
    if (this.$store.state.currentUser.displayname == undefined) {
      router.push('/login')
    } 

    // Otherwise...
    else {
      // Load the project summaries of the current user.
      this.updateProjectSummaries()

      // Initialize the countryList by picking out the (unique) country names.
      // (First, a list is constructed pulling out the non-unique countries 
      // for each project, then this array is stuffed into a new Set (which 
      // will not duplicate array entries) and then the spread operator is 
      // used to pull the set items out into an array.)
//      this.countryList = [...new Set(this.projectSummaries.map(theProj => theProj.country))]

      // Initialize the selection of the demo project to the first element.
//      this.selectedCountry = 'Select country...'
    }
  },

  methods: {
    updateProjectSummaries() {
      console.log('updateProjectSummaries() called')

      // Get the current user's project summaries from the server.
      rpcservice.rpcProjectCall('load_current_user_project_summaries')
      .then(response => {
        // Set the projects to what we received.
        this.projectSummaries = response.data.projects

        // Set select flags for false initially.
        this.projectSummaries.forEach(theProj => { theProj.selected = false })
      })

      // Get the demo project summaries from the server.
      rpcservice.rpcProjectCall('get_scirisdemo_projects')
      .then(response => {
        // Set the demo projects to what we received.
        this.demoProjectSummaries = response.data.projects

        // Initialize the demoProjectList by picking out the project names.
        this.demoProjectList = this.demoProjectSummaries.map(demoProj => demoProj.project.name)

        // Initialize the selection of the demo project to the first element.
        this.selectedDemoProject = this.demoProjectList[0]
      })
    },

    addDemoProject() {
      console.log('addDemoProject() called')

      // Find the object in the default project summaries that matches what's 
      // selected in the select box.
      let foundProject = this.demoProjectSummaries.find(demoProj => 
        demoProj.project.name == this.selectedDemoProject)

      // Make a deep copy of the found object by JSON-stringifying the old 
      // object, and then parsing the result back into a new object.
      let newProject = JSON.parse(JSON.stringify(foundProject));

      // Push the deep copy to the projectSummaries list.
//      this.projectSummaries.push(newProject)

//      this.projectSummaries.push(this.demoProjectSummaries[0])
    },

    createNewProject() {
      console.log('createNewProject() called')

      rpcservice.rpcProjectCall('tester_func_project', [0])
//      rpcservice.rpcProjectCall('tester_func_main', [0])
    },

    uploadProjectFromFile() {
      console.log('uploadProjectFromFile() called')
    },

    uploadProjectFromSpreadsheet() {
      console.log('uploadProjectFromSpreadsheet() called')
    },

    projectIsActive(uid) {
      // If the project is undefined, it is not active.
      if (this.$store.state.activeProject.project === undefined) {
        return false
      } 
   
      // Otherwise, the project is active if the UIDs match.
      else {
        return (this.$store.state.activeProject.project.id === uid)
      }
    },

    selectAll() {
      console.log('selectAll() called')

      // For each of the projects, set the selection of the project to the 
      // _opposite_ of the state of the all-select checkbox's state.
      // NOTE: This function depends on it getting called before the 
      // v-model state is updated.  If there are some cases of Vue 
      // implementation where these happen in the opposite order, then 
      // this will not give the desired result.
      this.projectSummaries.forEach(theProject => theProject.selected = !this.allSelected)
    },

    uncheckSelectAll() {
      this.allSelected = false
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

    applyNameFilter(projects) {
      console.log('applyNameFilter() called')

      return projects.filter(theProject => theProject.project.name.toLowerCase().indexOf(this.filterText.toLowerCase()) !== -1)
    },

    applySorting(projects) {
      console.log('applySorting() called')

      return projects.sort((proj1, proj2) => 
        {
          let sortDir = this.sortReverse ? -1: 1
          if (this.sortColumn === 'name') {
            return (proj1.project.name > proj2.project.name ? sortDir: -sortDir)
          }
/*          else if (this.sortColumn === 'country') {
            return proj1.country > proj2.country ? sortDir: -sortDir
          } */
          else if (this.sortColumn === 'creationTime') {
            return proj1.project.creationTime > proj2.project.creationTime ? sortDir: -sortDir
          }
          else if (this.sortColumn === 'updatedTime') {
            return proj1.project.updateTime > proj2.project.updateTime ? sortDir: -sortDir
          }
          else if (this.sortColumn === 'dataUploadTime') {
            return proj1.project.dataUploadTime > proj2.project.dataUploadTime ? sortDir: -sortDir
          } 
        }
      )
    },

/*    applyCountryFilter(projects) {
      console.log('applyCountryFilter() called')

      if (this.selectedCountry === 'Select country...')
        return projects
      else
        return projects.filter(theProj => theProj.country === this.selectedCountry)
    }, */

    openProject(uid) {
      // Find the project that matches the UID passed in.
      let matchProject = this.projectSummaries.find(theProj => theProj.project.id === uid)

      console.log('openProject() called for ' + matchProject.project.name)

      // Set the active project to the matched project.
      this.$store.commit('newActiveProject', matchProject)
    },

    copyProject(uid) {
      // Find the project that matches the UID passed in.
      let matchProject = this.projectSummaries.find(theProj => theProj.project.id === uid)

      console.log('copyProject() called for ' + matchProject.project.name)

//        rpcservice.rpcProjectCall('load_all_project_summaries', [matchProject.project.id])
        rpcservice.rpcProjectCall('load_all_project_summaries')
//      rpcservice.rpcProjectCall('tester_func_project', [matchProject.project.id])
//      rpcservice.rpcProjectCall('tester_func_main', [matchProject.project.id])
    },

    renameProject(uid) {
      // Find the project that matches the UID passed in.
      let matchProject = this.projectSummaries.find(theProj => theProj.project.id === uid)

      console.log('renameProject() called for ' + matchProject.project.name)
    },

    uploadSpreadsheetToProject(uid) {
      // Find the project that matches the UID passed in.
      let matchProject = this.projectSummaries.find(theProj => theProj.project.id === uid)

      console.log('uploadSpreadsheetToProject() called for ' + matchProject.project.name)
    },

    downloadSpreadsheetFromProject(uid) {
      // Find the project that matches the UID passed in.
      let matchProject = this.projectSummaries.find(theProj => theProj.project.id === uid)

      console.log('downloadSpreadsheetFromProject() called for ' + matchProject.project.name)
    },

    downloadProjectFile(uid) {
      // Find the project that matches the UID passed in.
      let matchProject = this.projectSummaries.find(theProj => theProj.project.id === uid)

      console.log('downloadProjectFile() called for ' + matchProject.project.name)
    },

    downloadProjectFileWithResults(uid) {
      // Find the project that matches the UID passed in.
      let matchProject = this.projectSummaries.find(theProj => theProj.project.id === uid)

      console.log('downloadProjectFileWithResults() called for ' + matchProject.project.name)
    },

    deleteSelectedProjects() {
      // Pull out the names of the projects that are selected.
      let selectProjects = this.projectSummaries.filter(theProj => 
        theProj.selected).map(theProj => theProj.project.name)

      console.log('deleteSelectedProjects() called for ', selectProjects)
    },

    downloadSelectedProjects() {
      // Pull out the names of the projects that are selected.
      let selectProjects = this.projectSummaries.filter(theProj => 
        theProj.selected).map(theProj => theProj.project.name)

      console.log('downloadSelectedProjects() called for ', selectProjects)
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style lang="scss" scoped>
</style>
