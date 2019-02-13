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
  import axios from 'axios'
  var filesaver = require('file-saver')
  import utils from '@/js/utils'
  import rpcs from '@/js/rpc-service'
  import status from '@/js/status-service'
  import router from '@/router'

  export default {
    name: 'ProjectsPage',

    data() {
      return {
        demoProjectList: [], // List of projects to choose from (by project name)
        selectedDemoProject: '', // Selected demo project (by name)
        demoProjectSummaries: [], // List of demo project summaries
        filterPlaceholder: 'Type here to filter projects', // Placeholder text for table filter box
        filterText: '', // Text in the table filter box
        allSelected: false, // Are all of the projects selected?
        projectToRename: null, // What project is being renamed?
        sortColumn: 'name',  // Column of table used for sorting the projects // name, country, creationTime, updatedTime, dataUploadTime
        sortReverse: false, // Sort in reverse order?
        projectSummaries: [], // List of summary objects for projects the user has
        countryList: [], // Available countries
        selectedCountry: 'Select country' // Country selected in the bottom select box
      }
    },

    computed: {
      sortedFilteredProjectSummaries() {
        return this.applyNameFilter(this.applySorting(this.projectSummaries))
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
      updateProjectSummaries(setActiveID) {
        console.log('updateProjectSummaries() called')
        status.start(this)
        rpcs.rpc('jsonify_projects', [this.$store.state.currentUser.username]) // Get the current user's project summaries from the server.
          .then(response => {
            let lastCreationTime = null
            let lastCreatedID = null
            this.projectSummaries = response.data.projects // Set the projects to what we received.
            if (this.projectSummaries.length > 0) { // Initialize the last creation time stuff if we have a non-empty list.
              lastCreationTime = this.projectSummaries[0].project.creationTime
              lastCreatedID = this.projectSummaries[0].project.id
            }
            this.projectToRename = null  // Unset the link to a project being renamed.
            this.projectSummaries.forEach(theProj => { // Preprocess all projects.
              theProj.selected = false // Set to not selected.
              theProj.renaming = '' // Set to not being renamed.
              console.log('hiiii!!!', 'id: ', theProj.project.id, 'new: ', theProj.project.creationTime, 'old: ', lastCreationTime, 'tf: ', theProj.project.creationTime >= lastCreationTime)
              if (theProj.project.creationTime >= lastCreationTime) { // Update the last creation time and ID if what se see is later.
                lastCreationTime = theProj.project.creationTime
                lastCreatedID = theProj.project.id
              }
            })
            if (this.projectSummaries.length > 0) { // If we have a project on the list...
              if (setActiveID === null) { // If no ID is passed in, set the active project to the last-created project.
                console.log('Opening last project', lastCreatedID)
                this.openProject(lastCreatedID)
              } else { // Otherwise, set the active project to the one passed in.
                console.log('Opening active project', setActiveID)
                this.openProject(setActiveID)
              }
            }
            status.succeed(this, '')  // No green popup.
          })
          .catch(error => {
            status.fail(this, 'Could not load projects', error)
          })
      },

      addDemoProject() {
        console.log('addDemoProject() called')
        status.start(this)
        rpcs.rpc('add_demo_project', [this.$store.state.currentUser.username]) // Have the server create a new project.
          .then(response => {
            this.updateProjectSummaries(null); // Update the project summaries so the new project shows up on the list.
            status.succeed(this, '') // Indicate success.
          })
          .catch(error => {
            status.fail(this, 'Could not add new project', error)    // Indicate failure.
          })
      },

      createNewProject() {
        console.log('createNewProject() called')
        status.start(this)
        rpcs.rpc('create_new_project', [this.$store.state.currentUser.username]) // Have the server create a new project.
          .then(response => {
            this.updateProjectSummaries(null); // Update the project summaries so the new project shows up on the list.
            status.succeed(this, '') // Indicate success.
          })
          .catch(error => {
            status.fail(this, 'Could not add new project', error)    // Indicate failure.
          })
      },

      uploadProjectFromFile() {
        console.log('uploadProjectFromFile() called')
        rpcs.upload('upload_project', [this.$store.state.currentUser.username], {}, '.prj') // Have the server upload the project.
          .then(response => {
            status.start(this)  // This line needs to be here to avoid the spinner being up during the user modal.
            this.updateProjectSummaries(response.data.projectID) // Update the project summaries so the new project shows up on the list.
            status.succeed(this, 'New project uploaded')
          })
          .catch(error => {
            status.fail(this, 'Could not upload file', error)
          })
      },

      projectIsActive(uid) {
        if (this.$store.state.activeProject.project === undefined) { // If the project is undefined, it is not active.
          return false
        } else { // Otherwise, the project is active if the UIDs match.
          return (this.$store.state.activeProject.project.id === uid)
        }
      },

      selectAll() {
        console.log('selectAll() called')
        this.projectSummaries.forEach(theProject => theProject.selected = !this.allSelected) // For each of the projects, set the selection of the project to the _opposite_ of the state of the all-select checkbox's state.
      },

      uncheckSelectAll() {
        this.allSelected = false
      },

      updateSorting(sortColumn) {
        console.log('updateSorting() called')
        if (this.sortColumn === sortColumn) { // If the active sorting column is clicked...
          this.sortReverse = !this.sortReverse // Reverse the sort.
        } else { // Otherwise.
          this.sortColumn = sortColumn // Select the new column for sorting.
          this.sortReverse = false // Set the sorting for non-reverse.
        }
      },

      applyNameFilter(projects) {
        return projects.filter(theProject => theProject.project.name.toLowerCase().indexOf(this.filterText.toLowerCase()) !== -1)
      },

      applySorting(projects) {
        return projects.slice(0).sort((proj1, proj2) =>
          {
            let sortDir = this.sortReverse ? -1: 1
            if (this.sortColumn === 'name') {
              return (proj1.project.name.toLowerCase() > proj2.project.name.toLowerCase() ? sortDir: -sortDir)
            } else if (this.sortColumn === 'creationTime') {
              return proj1.project.creationTime > proj2.project.creationTime ? sortDir: -sortDir
            } else if (this.sortColumn === 'updatedTime') {
              return proj1.project.updatedTime > proj2.project.updatedTime ? sortDir: -sortDir
            }
          }
        )
      },

      openProject(uid) {
        let matchProject = this.projectSummaries.find(theProj => theProj.project.id === uid) // Find the project that matches the UID passed in.
        console.log('openProject() called for ' + matchProject.project.name)
        this.$store.commit('newActiveProject', matchProject) // Set the active project to the matched project.
        status.succeed(this, 'Project "'+matchProject.project.name+'" loaded') // Success popup.
      },

      copyProject(uid) {
        let matchProject = this.projectSummaries.find(theProj => theProj.project.id === uid) // Find the project that matches the UID passed in.
        console.log('copyProject() called for ' + matchProject.project.name)
        status.start(this) // Start indicating progress.
        rpcs.rpc('copy_project', [uid]) // Have the server copy the project, giving it a new name.
          .then(response => {
            this.updateProjectSummaries(response.data.projectID) // Update the project summaries so the copied program shows up on the list.
            status.succeed(this, 'Project "'+matchProject.project.name+'" copied')    // Indicate success.
          })
          .catch(error => {
            status.fail(this, 'Could not copy project', error) // Indicate failure.
          })
      },

      finishRename(event) {
        // Grab the element of the open textbox for the project name to be renamed.
        let renameboxElem = document.querySelector('.renamebox')

        // If the click is outside the textbox, rename the remembered project.
        if (!renameboxElem.contains(event.target)) {
          this.renameProject(this.projectToRename)
        }
      },

      renameProject(projectSummary) {
        console.log('renameProject() called for ' + projectSummary.project.name)
        if (projectSummary.renaming === '') { // If the project is not in a mode to be renamed, make it so.
          projectSummary.renaming = projectSummary.project.name
          // Add a click listener to run the rename when outside the input box is click, and remember
          // which project needs to be renamed.
          window.addEventListener('click', this.finishRename)
          this.projectToRename = projectSummary
        } else { // Otherwise (it is to be renamed)...
          // Remove the listener for reading the clicks outside the input box, and null out the project
          // to be renamed.
          window.removeEventListener('click', this.finishRename)
          this.projectToRename = null
          let newProjectSummary = _.cloneDeep(projectSummary) // Make a deep copy of the projectSummary object by JSON-stringifying the old object, and then parsing the result back into a new object.
          newProjectSummary.project.name = projectSummary.renaming // Rename the project name in the client list from what's in the textbox.
          status.start(this)
          rpcs.rpc('rename_project', [newProjectSummary]) // Have the server change the name of the project by passing in the new copy of the summary.
            .then(response => {
              this.updateProjectSummaries(newProjectSummary.project.id) // Update the project summaries so the rename shows up on the list.
              projectSummary.renaming = '' // Turn off the renaming mode.
              status.succeed(this, '')  // No green popup message.
            })
            .catch(error => {
              status.fail(this, 'Could not rename project', error) // Indicate failure.
            })
        }

        // This silly hack is done to make sure that the Vue component gets updated by this function call.
        // Something about resetting the project name informs the Vue component it needs to
        // update, whereas the renaming attribute fails to update it.
        // We should find a better way to do this.
        let theName = projectSummary.project.name
        projectSummary.project.name = 'newname'
        projectSummary.project.name = theName
      },

      downloadProjectFile(uid) {
        let matchProject = this.projectSummaries.find(theProj => theProj.project.id === uid) // Find the project that matches the UID passed in.
        console.log('downloadProjectFile() called for ' + matchProject.project.name)
        status.start(this) // Start indicating progress.
        rpcs.download('download_project', [uid]) // Make the server call to download the project to a .prj file.
          .then(response => { // Indicate success.
            status.succeed(this, '')  // No green popup message.
          })
          .catch(error => { // Indicate failure.
            status.fail(this, 'Could not download project', error)
          })
      },

      // Confirmation alert
      deleteModal() {
        let selectProjectsUIDs = this.projectSummaries.filter(theProj => // Pull out the names of the projects that are selected.
          theProj.selected).map(theProj => theProj.project.id)
        if (selectProjectsUIDs.length > 0) { // Only if something is selected...
          var obj = { // Alert object data
            message: 'Are you sure you want to delete the selected projects?',
            useConfirmBtn: true,
            customConfirmBtnClass: 'btn __red',
            customCloseBtnClass: 'btn',
            onConfirm: this.deleteSelectedProjects
          }
          this.$Simplert.open(obj)
        }
      },

      deleteSelectedProjects() {
        let selectProjectsUIDs = this.projectSummaries.filter(theProj => // Pull out the names of the projects that are selected.
          theProj.selected).map(theProj => theProj.project.id)
        console.log('deleteSelectedProjects() called for ', selectProjectsUIDs)
        if (selectProjectsUIDs.length > 0) { // Have the server delete the selected projects.
          status.start(this)
          rpcs.rpc('delete_projects', [selectProjectsUIDs])
            .then(response => {
              let activeProjectId = this.$store.state.activeProject.project.id // Get the active project ID.
              if (activeProjectId === undefined) {
                activeProjectId = null
              }
              if (selectProjectsUIDs.find(theId => theId === activeProjectId)) { // If the active project ID is one of the ones deleted...
                this.$store.commit('newActiveProject', {}) // Set the active project to an empty project.
                activeProjectId = null // Null out the project.
              }
              this.updateProjectSummaries(activeProjectId) // Update the project summaries so the deletions show up on the list. Make sure it tries to set the project that was active (if any).
              status.succeed(this, '')  // No green popup message.
            })
            .catch(error => {
              status.fail(this, 'Could not delete project(s)', error)
            })
        }
      },

      downloadSelectedProjects() {
        let selectProjectsUIDs = this.projectSummaries.filter(theProj => // Pull out the names of the projects that are selected.
          theProj.selected).map(theProj => theProj.project.id)
        console.log('downloadSelectedProjects() called for ', selectProjectsUIDs)
        if (selectProjectsUIDs.length > 0) { // Have the server download the selected projects.
          status.start(this)
          rpcs.download('download_projects', [selectProjectsUIDs, this.$store.state.currentUser.username])
            .then(response => {
              // Indicate success.
              status.succeed(this, '')  // No green popup message.
            })
            .catch(error => {
              status.fail(this, 'Could not download project(s)', error) // Indicate failure.
            })
        }
      }
    }
  }
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style lang="scss" scoped>
</style>
