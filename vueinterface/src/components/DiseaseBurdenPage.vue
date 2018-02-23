<!-- 
DiseaseBurdenPage.vue -- DiseaseBurdenPage Vue component

Last update: 2/22/18 (gchadder3)
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
      activeProject: {}
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
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style lang="scss" scoped>
</style>
