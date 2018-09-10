<!--
Manage projects page

Last update: 2018-07-27
-->

<template>
  <div class="SitePage">
    <div class="PageSection">

      <div class="ControlsRow">
        <button class="btn" @click="createNewProject">Create new project</button>
        &nbsp; &nbsp;
        <button class="btn" @click="uploadProjectFromFile">Upload project from file</button>
        &nbsp; &nbsp;
      </div>
    </div>

    <div class="PageSection"
         v-if="projectSummaries.length > 0">
      <!--<h2>Manage projects</h2>-->

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
          <td>
            <input type="checkbox" @click="uncheckSelectAll()" v-model="projectSummary.selected"/>
          </td>
          <td v-if="projectSummary.renaming !== ''">
            <input type="text"
                   class="txbox"
                   @keyup.enter="renameProject(projectSummary)"
                   v-model="projectSummary.renaming"/>
          </td>
          <td v-else>
            {{ projectSummary.project.name }}
          </td>
          <td>
            <button class="btn __green" @click="openProject(projectSummary.project.id)">Open</button>
          </td>
          <!--            <td>{{ projectSummary.country }}</td> -->
          <td>{{ projectSummary.project.creationTime.toUTCString() }}</td>
          <td>{{ projectSummary.project.updatedTime ? projectSummary.project.updatedTime.toUTCString():
            'No modification' }}</td>
          <td style="white-space: nowrap">
            <button class="btn" @click="copyProject(projectSummary.project.id)">Copy</button>
            <button class="btn" @click="renameProject(projectSummary)">Rename</button>
            <button class="btn" @click="downloadProjectFile(projectSummary.project.id)">Download</button>
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
        <button class="btn" @click="deleteModal()">Delete selected</button>
        &nbsp; &nbsp;
        <button class="btn" @click="downloadSelectedProjects">Download selected</button>
      </div>
    </div>

    <!-- Popup spinner -->
    <modal name="popup-spinner"
           height="80px"
           width="85px"
           style="opacity: 0.6">
      <clip-loader color="#0000ff"
                   size="50px"
                   style="padding: 15px">
      </clip-loader>
    </modal>

  </div>
</template>

<script>
  import axios from 'axios'
  var filesaver = require('file-saver')
  import rpcs from '@/services/rpc-service'
  import router from '@/router'
  import ClipLoader from 'vue-spinner/src/ClipLoader.vue'

  export default {
    name: 'ProjectsPage',

    components: {
      ClipLoader
    },

    data() {
      return {
        // List of projects to choose from (by project name)
        demoProjectList: [],

        // Selected demo project (by name)
        selectedDemoProject: '',

        // List of demo project summaries
        demoProjectSummaries: [],

        // Placeholder text for table filter box
        filterPlaceholder: 'Type here to filter projects',

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
      let projectId = null

      // If we have no user logged in, automatically redirect to the login page.
      if (this.$store.state.currentUser.displayname == undefined) {
        router.push('/login')
      }

      // Otherwise...
      else {
        // Get the active project ID if there is an active project.
        if (this.$store.state.activeProject.project != undefined) {
          projectId = this.$store.state.activeProject.project.id
        }

        // Load the project summaries of the current user.
        this.updateProjectSummaries(projectId)

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
      updateProjectSummaries(setActiveID) {
        console.log('updateProjectSummaries() called')

        // Get the current user's project summaries from the server.
        rpcs.rpc('load_current_user_project_summaries')
          .then(response => {
            let lastCreationTime = null
            let lastCreatedID = null

            // Set the projects to what we received.
            this.projectSummaries = response.data.projects

            // Initialize the last creation time stuff if we have a non-empty list.
            if (this.projectSummaries.length > 0) {
              lastCreationTime = new Date(this.projectSummaries[0].project.creationTime)
              lastCreatedID = this.projectSummaries[0].project.id
            }

            // Preprocess all projects.
            this.projectSummaries.forEach(theProj => {
              // Set to not selected.
              theProj.selected = false

              // Set to not being renamed.
              theProj.renaming = ''

              // Extract actual Date objects from the strings.
              theProj.project.creationTime = new Date(theProj.project.creationTime)
              theProj.project.updatedTime = new Date(theProj.project.updatedTime)

              // Update the last creation time and ID if what se see is later.
              if (theProj.project.creationTime >= lastCreationTime) {
                lastCreationTime = theProj.project.creationTime
                lastCreatedID = theProj.project.id
              }
            })

            // If we have a project on the list...
            if (this.projectSummaries.length > 0) {
              // If no ID is passed in, set the active project to the last-created
              // project.
              if (setActiveID == null) {
                this.openProject(lastCreatedID)
              }

              // Otherwise, set the active project to the one passed in.
              else {
                this.openProject(setActiveID)
              }
            }
          })
          .catch(error => {
            // Failure popup.
            this.$notifications.notify({
              message: 'Could not load projects',
              icon: 'ti-face-sad',
              type: 'warning',
              verticalAlign: 'top',
              horizontalAlign: 'center',
            })
          })
      },

      /*    addDemoProject() {
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
       }, */

      createNewProject() {
        console.log('createNewProject() called')

        // Bring up a spinner.
        this.$modal.show('popup-spinner')

        // Start the loading bar.
        this.$Progress.start()

        // Have the server create a new project.
        rpcs.rpc('create_new_project', [this.$store.state.currentUser.UID])
          .then(response => {
            // Update the project summaries so the new project shows up on the list.
            // Note: There's no easy way to get the new project UID to tell the
            // project update to choose the new project because the RPC cannot pass
            // it back.
            this.updateProjectSummaries(null)

            // Dispel the spinner.
            this.$modal.hide('popup-spinner')

            // Finish the loading bar.
            this.$Progress.finish()

            // Success popup.
            this.$notifications.notify({
              message: 'New project created',
              icon: 'ti-check',
              type: 'success',
              verticalAlign: 'top',
              horizontalAlign: 'center',
            })
          })
          .catch(error => {
            // Dispel the spinner.
            this.$modal.hide('popup-spinner')

            // Fail the loading bar.
            this.$Progress.fail()

            // Failure popup.
            this.$notifications.notify({
              message: 'Could not add new project',
              icon: 'ti-face-sad',
              type: 'warning',
              verticalAlign: 'top',
              horizontalAlign: 'center',
            })
          })
      },

      uploadProjectFromFile() {
        console.log('uploadProjectFromFile() called')

        // Have the server upload the project.
        rpcs.upload('create_project_from_prj_file', [this.$store.state.currentUser.UID], {}, '.prj')
          .then(response => {
            // Bring up a spinner.
            this.$modal.show('popup-spinner')

            // Start the loading bar.  (This is here because we don't want the
            // progress bar running when the user is picking a file to upload.)
            this.$Progress.start()

            // Update the project summaries so the new project shows up on the list.
            this.updateProjectSummaries(response.data.projectId)

            // Dispel the spinner.
            this.$modal.hide('popup-spinner')

            // Finish the loading bar.
            this.$Progress.finish()

            // Success popup.
            this.$notifications.notify({
              message: 'New project uploaded',
              icon: 'ti-check',
              type: 'success',
              verticalAlign: 'top',
              horizontalAlign: 'center',
            })
          })
          .catch(error => {
            // Dispel the spinner.
            this.$modal.hide('popup-spinner')

            // Fail the loading bar.
            this.$Progress.fail()

            // Failure popup.
            this.$notifications.notify({
              message: 'Could not upload file',
              icon: 'ti-face-sad',
              type: 'warning',
              verticalAlign: 'top',
              horizontalAlign: 'center',
            })
          })
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
        return projects.filter(theProject => theProject.project.name.toLowerCase().indexOf(this.filterText.toLowerCase()) !== -1)
      },

      applySorting(projects) {
        return projects.slice(0).sort((proj1, proj2) =>
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
              return proj1.project.updatedTime > proj2.project.updatedTime ? sortDir: -sortDir
            }
          }
        )
      },

      /*    applyCountryFilter(projects) {
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

        // Success popup.
        this.$notifications.notify({
          message: 'Project "'+matchProject.project.name+'" loaded',
          icon: 'ti-check',
          type: 'success',
          verticalAlign: 'top',
          horizontalAlign: 'center',
        });
      },

      copyProject(uid) {
        // Find the project that matches the UID passed in.
        let matchProject = this.projectSummaries.find(theProj => theProj.project.id === uid)

        console.log('copyProject() called for ' + matchProject.project.name)

        // Bring up a spinner.
        this.$modal.show('popup-spinner')

        // Start the loading bar.
        this.$Progress.start()

        // Have the server copy the project, giving it a new name.
        rpcs.rpc('copy_project', [uid])
          .then(response => {
            // Update the project summaries so the copied program shows up on the list.
            this.updateProjectSummaries(response.data.projectId)

            // Dispel the spinner.
            this.$modal.hide('popup-spinner')

            // Finish the loading bar.
            this.$Progress.finish()

            // Success popup.
            this.$notifications.notify({
              message: 'Project "'+matchProject.project.name+'" copied',
              icon: 'ti-check',
              type: 'success',
              verticalAlign: 'top',
              horizontalAlign: 'center',
            })
          })
          .catch(error => {
            // Dispel the spinner.
            this.$modal.hide('popup-spinner')

            // Fail the loading bar.
            this.$Progress.fail()

            // Failure popup.
            this.$notifications.notify({
              message: 'Could not copy project',
              icon: 'ti-face-sad',
              type: 'warning',
              verticalAlign: 'top',
              horizontalAlign: 'center',
            })
          })
      },

      renameProject(projectSummary) {
        console.log('renameProject() called for ' + projectSummary.project.name)

        // If the project is not in a mode to be renamed, make it so.
        if (projectSummary.renaming === '') {
          projectSummary.renaming = projectSummary.project.name
        }

        // Otherwise (it is to be renamed)...
        else {
          // Make a deep copy of the projectSummary object by JSON-stringifying the old
          // object, and then parsing the result back into a new object.
          let newProjectSummary = JSON.parse(JSON.stringify(projectSummary))

          // Rename the project name in the client list from what's in the textbox.
          newProjectSummary.project.name = projectSummary.renaming

          // Bring up a spinner.
          this.$modal.show('popup-spinner')

          // Start the loading bar.
          this.$Progress.start()

          // Have the server change the name of the project by passing in the new copy of the
          // summary.
          rpcs.rpc('update_project_from_summary', [newProjectSummary])
            .then(response => {
              // Update the project summaries so the rename shows up on the list.
              this.updateProjectSummaries(newProjectSummary.project.id)

              // Turn off the renaming mode.
              projectSummary.renaming = ''

              // Dispel the spinner.
              this.$modal.hide('popup-spinner')

              // Finish the loading bar.
              this.$Progress.finish()
            })
            .catch(error => {
              // Dispel the spinner.
              this.$modal.hide('popup-spinner')

              // Fail the loading bar.
              this.$Progress.fail()

              // Failure popup.
              this.$notifications.notify({
                message: 'Could not rename project',
                icon: 'ti-face-sad',
                type: 'warning',
                verticalAlign: 'top',
                horizontalAlign: 'center',
              })
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
        // Find the project that matches the UID passed in.
        let matchProject = this.projectSummaries.find(theProj => theProj.project.id === uid)

        console.log('downloadProjectFile() called for ' + matchProject.project.name)

        // Bring up a spinner.
        this.$modal.show('popup-spinner')

        // Start the loading bar.
        this.$Progress.start()

        // Make the server call to download the project to a .prj file.
        rpcs.download('download_project', [uid])
          .then(response => {
            // Dispel the spinner.
            this.$modal.hide('popup-spinner')

            // Finish the loading bar.
            this.$Progress.finish()
          })
          .catch(error => {
            // Dispel the spinner.
            this.$modal.hide('popup-spinner')

            // Fail the loading bar.
            this.$Progress.fail()

            // Failure popup.
            this.$notifications.notify({
              message: 'Could not download project',
              icon: 'ti-face-sad',
              type: 'warning',
              verticalAlign: 'top',
              horizontalAlign: 'center',
            })
          })
      },

      // Confirmation alert
      deleteModal() {
        // Pull out the names of the projects that are selected.
        let selectProjectsUIDs = this.projectSummaries.filter(theProj =>
          theProj.selected).map(theProj => theProj.project.id)

        // Only if something is selected...
        if (selectProjectsUIDs.length > 0) {
          // Alert object data
          var obj = {
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
        // Pull out the names of the projects that are selected.
        let selectProjectsUIDs = this.projectSummaries.filter(theProj =>
          theProj.selected).map(theProj => theProj.project.id)

        console.log('deleteSelectedProjects() called for ', selectProjectsUIDs)

        // Have the server delete the selected projects.
        if (selectProjectsUIDs.length > 0) {
          // Bring up a spinner.
          this.$modal.show('popup-spinner')

          // Start the loading bar.
          this.$Progress.start()

          rpcs.rpc('delete_projects', [selectProjectsUIDs])
            .then(response => {
              // Get the active project ID.
              let activeProjectId = this.$store.state.activeProject.project.id
              if (activeProjectId === undefined) {
                activeProjectId = null
              }

              // If the active project ID is one of the ones deleted...
              if (selectProjectsUIDs.find(theId => theId === activeProjectId)) {
                // Set the active project to an empty project.
                this.$store.commit('newActiveProject', {})

                // Null out the project.
                activeProjectId = null
              }

              // Update the project summaries so the deletions show up on the list.
              // Make sure it tries to set the project that was active (if any).
              this.updateProjectSummaries(activeProjectId)

              // Dispel the spinner.
              this.$modal.hide('popup-spinner')

              // Finish the loading bar.
              this.$Progress.finish()
            })
            .catch(error => {
              // Dispel the spinner.
              this.$modal.hide('popup-spinner')

              // Fail the loading bar.
              this.$Progress.fail()

              // Failure popup.
              this.$notifications.notify({
                message: 'Could not delete project/s',
                icon: 'ti-face-sad',
                type: 'warning',
                verticalAlign: 'top',
                horizontalAlign: 'center',
              })
            })
        }
      },

      downloadSelectedProjects() {
        // Pull out the names of the projects that are selected.
        let selectProjectsUIDs = this.projectSummaries.filter(theProj =>
          theProj.selected).map(theProj => theProj.project.id)

        console.log('deleteSelectedProjects() called for ', selectProjectsUIDs)

        // Have the server download the selected projects.
        if (selectProjectsUIDs.length > 0) {
          // Bring up a spinner.
          this.$modal.show('popup-spinner')

          // Start the loading bar.
          this.$Progress.start()

          rpcs.download('load_zip_of_prj_files', [selectProjectsUIDs])
            .then(response => {
              // Dispel the spinner.
              this.$modal.hide('popup-spinner')

              // Finish the loading bar.
              this.$Progress.finish()
            })
            .catch(error => {
              // Dispel the spinner.
              this.$modal.hide('popup-spinner')

              // Fail the loading bar.
              this.$Progress.fail()

              // Failure popup.
              this.$notifications.notify({
                message: 'Could not download project/s',
                icon: 'ti-face-sad',
                type: 'warning',
                verticalAlign: 'top',
                horizontalAlign: 'center',
              })
            })
        }
      }
    }
  }
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style lang="scss" scoped>
</style>
