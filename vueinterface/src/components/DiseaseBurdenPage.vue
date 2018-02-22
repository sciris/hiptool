<!-- 
DiseaseBurdenPage.vue -- DiseaseBurdenPage Vue component

Last update: 2/21/18 (gchadder3)
-->

<template>
  <div class="SitePage">
    <h2>Disease Burden Page</h2>

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
            <th @click="updateSorting('country')" class="sortable">
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
          <tr v-for="projectSummary in sortedFilteredProjectSummaries" :class="{ highlighted: activeProject.uid === projectSummary.uid }">
            <td>{{ projectSummary.projectName }}</td>
            <td>{{ projectSummary.country }}</td>
            <td>{{ projectSummary.creationTime }}</td>
            <td>{{ projectSummary.updateTime ? projectSummary.updateTime: 
              'No modification' }}</td>
            <td style="white-space: nowrap">
              <button class="btn __green" @click="openProject(projectSummary.uid)">Open</button>
              <button class="btn" @click="copyProject(projectSummary.uid)">Copy</button>
              <button class="btn" @click="renameProject(projectSummary.uid)">Rename</button>
              <button class="btn __red" @click="deleteProject(projectSummary.uid)">Delete</button>
            </td>
          </tr>
          <tr>
            <td>
              <button class="btn" @click="createNewProject">Create new project</button>
            </td>
            <td>
              <select v-model="selectedCountry">
                <option>Select country...</option>
                <option v-for="choice in countryList">
                  {{ choice }}
                </option>
              </select>
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
      sortColumn: 'name',  // name, country, creationTime, updatedTime

      // Sort in reverse order?
      sortReverse: false, 

      // List of summary objects for projects the user has
      projectSummaries: 
        [
          {
            projectName: 'Afghanistan test 1',
            country: 'Afghanistan', 
            creationTime: '2017-Sep-21 08:44 AM',
            updateTime: '2017-Sep-21 08:44 AM',
            uid: 1,
            selected: false
          }, 
          {
            projectName: 'Afghanistan HBP equity',
            country: 'Afghanistan', 
            creationTime: '2017-Sep-22 08:44 AM',
            updateTime: '',
            uid: 2,
            selected: false
          },
          {
            projectName: 'Final Afghanistan HBP', 
            country: 'Afghanistan', 
            creationTime: '2017-Sep-21 08:44 AM',
            updateTime: '2017-Sep-21 08:44 AM',
            uid: 3,
            selected: false
          },
          {
            projectName: 'Pakistan test 1',
            country: 'Pakistan', 
            creationTime: '2017-Sep-21 08:44 AM',
            updateTime: '2017-Sep-21 08:44 AM',
            uid: 4,
            selected: false
          }
        ],

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
      return this.applyNameFilter(this.applySorting(this.applyCountryFilter(this.projectSummaries)))
    } 
  }, 

  created() {
    // If we have no user logged in, automatically redirect to the login page.
    if (this.$store.state.currentuser.displayname == undefined) {
      router.push('/login')
    } 

    // Otherwise...
    else {
      // Initialize the countryList by picking out the (unique) country names.
      // (First, a list is constructed pulling out the non-unique countries 
      // for each project, then this array is stuffed into a new Set (which 
      // will not duplicate array entries) and then the spread operator is 
      // used to pull the set items out into an array.)
      this.countryList = [...new Set(this.projectSummaries.map(theProj => theProj.country))]

      // Initialize the selection of the demo project to the first element.
      this.selectedCountry = 'Select country...'
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

    applyCountryFilter(projects) {
      console.log('applyCountryFilter() called')

      if (this.selectedCountry === 'Select country...')
        return projects
      else
        return projects.filter(theProj => theProj.country === this.selectedCountry)
    },

    openProject(uid) {
      // Find the project that matches the UID passed in.
      let matchProject = this.projectSummaries.find(theProj => theProj.uid === uid)

      console.log('openProject() called for ' + matchProject.projectName)

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
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style lang="scss" scoped>
</style>
