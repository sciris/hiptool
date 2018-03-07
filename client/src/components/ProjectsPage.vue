<!-- 
ProjectsPage.vue -- ProjectsPage Vue component

Last update: 3/6/18 (gchadder3)
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
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="projectSummary in sortedFilteredProjectSummaries" 
              :class="{ highlighted: projectIsActive(projectSummary.project.id) }">
            <td>{{ projectSummary.project.name }}</td>
<!--            <td>{{ projectSummary.country }}</td> -->
            <td>{{ projectSummary.project.creationTime }}</td>
            <td>{{ projectSummary.project.updatedTime ? projectSummary.project.updatedTime: 
              'No modification' }}</td>
            <td style="white-space: nowrap">
              <button class="btn __green" @click="openProject(projectSummary.project.id)">Open</button>
              <button class="btn" @click="copyProject(projectSummary.project.id)">Copy</button>
              <button class="btn" @click="renameProject(projectSummary.project.id)">Rename</button>
              <button class="btn __red" @click="deleteProject(projectSummary.project.id)">Delete</button>
            </td>
          </tr>
          <tr>
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
            </td> -->
          </tr>
        </tbody>
      </table>
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

      // Active project
      activeProject: {},

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
    if (this.$store.state.currentuser.displayname == undefined) {
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
        this.projectSummaries = response.data.projects
      })
    },

    projectIsActive(uid) {
      // If the project is undefined, it is not active.
      if (this.activeProject.project === undefined) {
        return false
      } 
   
      // Otherwise, the project is active if the UIDs match.
      else {
        return (this.activeProject.project.id === uid)
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
      this.activeProject = matchProject
    },

    copyProject(uid) {
      // Find the project that matches the UID passed in.
      let matchProject = this.projectSummaries.find(theProj => theProj.project.id === uid)

      console.log('copyProject() called for ' + matchProject.project.name)
    },

    renameProject(uid) {
      // Find the project that matches the UID passed in.
      let matchProject = this.projectSummaries.find(theProj => theProj.project.id === uid)

      console.log('renameProject() called for ' + matchProject.project.name)
    },

    deleteProject(uid) {
      // Find the project that matches the UID passed in.
      let matchProject = this.projectSummaries.find(theProj => theProj.project.id === uid)

      console.log('deleteProject() called for ' + matchProject.projectName)
    },

    createNewProject() {
      console.log('createNewProject() called')
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style lang="scss" scoped>
</style>
