<!--
Manage projects page

Last update: 2018oct04
-->

<template>
  <div class="SitePage">
    <div class="PageSection">

      <div class="ControlsRow">
        <button class="btn" @click="createNewProject">Create new project</button>
        &nbsp; &nbsp;
        <button class="btn" @click="addDemoProject">Add demo project</button>
        &nbsp; &nbsp;

        <button class="btn" @click="uploadProjectFromFile">Upload project from file</button>
        &nbsp; &nbsp;
      </div>
    </div>

    <div class="PageSection" v-if="projectSummaries.length > 0">

      <input type="text"
             class="txbox"
             style="margin-bottom: 20px"
             :placeholder="filterPlaceholder"
             v-model="filterText"/>

      <table class="table table-bordered table-hover table-striped" style="width: 100%">
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
          <td>
            <input type="checkbox" @click="uncheckSelectAll()" v-model="projectSummary.selected"/>
          </td>
          <td v-if="projectSummary.renaming !== ''">
            <input type="text"
                   class="txbox renamebox"
                   @keyup.enter="renameProject(projectSummary)"
                   v-model="projectSummary.renaming"/>
          </td>
          <td v-else>
            <b>{{ projectSummary.project.name }}</b>
          </td>
          <td>
            <button class="btn __green" @click="openProject(projectSummary.project.id)">Open</button>
          </td>
          <td>{{ projectSummary.project.creationTime }}</td>
          <td>{{ projectSummary.project.updatedTime ? projectSummary.project.updatedTime:
            'No modification' }}</td>
          <td style="white-space: nowrap">
            <button class="btn" @click="copyProject(projectSummary.project.id)">Copy</button>
            <button class="btn" @click="renameProject(projectSummary)">Rename</button>
            <button class="btn" @click="downloadProjectFile(projectSummary.project.id)">Download</button>
          </td>
        </tr>
        </tbody>
      </table>

      <div class="ControlsRow">
        <button class="btn" @click="deleteModal()">Delete selected</button>&nbsp; &nbsp;
        <button class="btn" @click="downloadSelectedProjects">Download selected</button>
      </div>
    </div>

  </div>
</template>

<script>
import { mixins } from 'sciris-uikit';
import sciris from 'sciris-js';
import router from '../router.js'

export default {
  name: 'ProjectsPage',
  mixins: [
    mixins.ProjectMixin 
  ],
  data() {
    return {
      demoProjectList: [], // List of projects to choose from (by project name)
      selectedDemoProject: '', // Selected demo project (by name)
      demoProjectSummaries: [], // List of demo project summaries
      countryList: [], // Available countries
      selectedCountry: 'Select country' // Country selected in the bottom select box
    }
  },
  created() {
    let projectID = null
    if (this.$store.state.currentUser.displayname === undefined) { // If we have no user logged in, automatically redirect to the login page.
      router.push('/login')
    } else { // Otherwise...
      if (this.$store.state.activeProject.project !== undefined) { // Get the active project ID if there is an active project.
        projectID = this.$store.state.activeProject.project.id
      }
      this.updateProjectSummaries(projectID) // Load the project summaries of the current user.
    }
  },
  methods: {
    toolName: function(){
      return this.$toolName; 
    },
    getFrameworkID: function(){
      return null;
    },
    getAppRouter: function(){
      return router;
    },
    addDemoProject() {
      console.log('addDemoProject() called')
      sciris.start(this)
      sciris.rpc('add_demo_project', [
        this.userName
      ]) // Have the server create a new project.
      .then(response => {
        this.updateProjectSummaries(null); // Update the project summaries so the new project shows up on the list.
        sciris.succeed(this, '') // Indicate success.
      })
      .catch(error => {
        sciris.fail(this, 'Could not add new project', error)    // Indicate failure.
      })
    },
  }
}
</script>
