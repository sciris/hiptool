<!--
Define interventions

Last update: 2018oct04
-->

<template>
  <div class="SitePage">

    <div v-if="activeProjectName === ''">
      <div style="font-style:italic">
        <p>Hmm, I can't find any interventions...did you forget to <router-link to="/projects">load a project</router-link>?</p>
      </div>
    </div>

    <div class="PageSection" v-if="activeProjectName !== ''">

      <button class="btn __green" @click="createNewSet">Create new intervention set</button>
      <span>&nbsp;based on&nbsp;</span>
      <select
        title="countrySelect"
        id="country"
        :required="true"
        v-model="country">
        <option v-for = "country in countryList" :value="country">
          {{country}}
        </option>
      </select>

      <br/><br/>

      <input type="text"
             class="txbox"
             style="margin-left:0px; margin-bottom:10px; display:inline-block; width:100%"
             :placeholder="filterPlaceholder"
             v-model="filterText"/>

      <table class="table table-bordered table-hover table-striped" style="width: 100%">
        <thead>
        <tr>
          <th @click="updateSorting('name')" class="sortable">
            Intervention set
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
          <th>
            Select
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
            <span v-show="sortColumn == 'updatedTime' && !sortReverse"><i class="fas fa-caret-down"></i></span>
            <span v-show="sortColumn == 'updatedTime' && sortReverse"><i class="fas fa-caret-up"></i></span>
            <span v-show="sortColumn != 'updatedTime'"><i class="fas fa-caret-up" style="visibility: hidden"></i></span>
          </th>
          <th>Actions</th>
        </tr>
        </thead>
        <tbody>
        <tr v-for="intervSet in sortedFilteredIntervSets"
            :class="{ highlighted: intervSetIsSelected(intervSet) }">
          <td v-if="intervSet.renaming !== ''">
            <input type="text"
                   class="txbox renamebox"
                   @keyup.enter="renameSet(intervSet)"
                   v-model="intervSet.renaming"/>
          </td>
          <td v-else>
            {{ intervSet.intervset.name }}
          </td>
          <td>
            <button class="btn" @click="viewSet(intervSet, true)">Open</button>
          </td>
          <td>{{ intervSet.intervset.creationTime }}</td>
          <td>{{ intervSet.intervset.updateTime ? intervSet.intervset.updateTime:
            'No modification' }}</td>
          <td style="white-space: nowrap">
            <button class="btn" @click="copySet(intervSet)">Copy</button>
            <button class="btn" @click="renameSet(intervSet)">Rename</button>
            <button class="btn" @click="uploadIntervSet(intervSet)">Upload</button>
            <button class="btn" @click="downloadIntervSet(intervSet)">Download</button>
            <button class="btn __red" @click="deleteSet(intervSet)">Delete</button>
          </td>
        </tr>
        </tbody>
      </table>
    </div>


    <div class="PageSection" v-if="activeIntervSet.intervset != undefined">
      <input type="text"
             class="txbox"
             style="margin-left:0px; margin-bottom:10px; display:inline-block; width:100%"
             :placeholder="filterPlaceholder2"
             v-model="filterText2"/>

      <table class="table table-bordered table-hover table-striped scrolltable" style="width: auto; margin-top: 10px">
        <thead>
        <tr>
          <th>Active</th>
          <th @click="updateSorting2('name')" class="sortable" style="min-width:30%">
            Intervention&nbsp;name
            <span v-show="sortColumn2 == 'name' && !sortReverse2"><i class="fas fa-caret-down"></i></span>
            <span v-show="sortColumn2 == 'name' && sortReverse2"><i class="fas fa-caret-up"></i></span>
            <span v-show="sortColumn2 != 'name'"><i class="fas fa-caret-up" style="visibility: hidden"></i></span>
          </th>
          <th @click="updateSorting2('platform')" class="sortable" style="min-width:30%">
            Delivery&nbsp;platform
            <span v-show="sortColumn2 == 'platform' && !sortReverse2"><i class="fas fa-caret-down"></i></span>
            <span v-show="sortColumn2 == 'platform' && sortReverse2"><i class="fas fa-caret-up"></i></span>
            <span v-show="sortColumn2 != 'platform'"><i class="fas fa-caret-up" style="visibility: hidden"></i></span>
          </th>
          <th @click="updateSorting2('burdencov')" class="sortable" style="min-width:30%">
            Cause&nbsp;of&nbsp;burden&nbsp;(max&nbsp;coverage)
            <span v-show="sortColumn2 == 'burdencov' && !sortReverse2"><i class="fas fa-caret-down"></i></span>
            <span v-show="sortColumn2 == 'burdencov' && sortReverse2"><i class="fas fa-caret-up"></i></span>
            <span v-show="sortColumn2 != 'burdencov'"><i class="fas fa-caret-up" style="visibility: hidden"></i></span>
          </th>
          <th @click="updateSorting2('icer')" class="sortable rightalign" style="min-width:30%">
            ICER
            <span v-show="sortColumn2 == 'icer' && !sortReverse2"><i class="fas fa-caret-down"></i></span>
            <span v-show="sortColumn2 == 'icer' && sortReverse2"><i class="fas fa-caret-up"></i></span>
            <span v-show="sortColumn2 != 'icer'"><i class="fas fa-caret-up" style="visibility: hidden"></i></span>
          </th>
          <th @click="updateSorting2('unitcost')" class="sortable rightalign" style="min-width:30%">
            Unit&nbsp;cost
            <span v-show="sortColumn2 == 'unitcost' && !sortReverse2"><i class="fas fa-caret-down"></i></span>
            <span v-show="sortColumn2 == 'unitcost' && sortReverse2"><i class="fas fa-caret-up"></i></span>
            <span v-show="sortColumn2 != 'unitcost'"><i class="fas fa-caret-up" style="visibility: hidden"></i></span>
          </th>
          <th @click="updateSorting2('spend')" class="sortable rightalign" style="min-width:30%">
            Spending
            <span v-show="sortColumn2 == 'spend' && !sortReverse2"><i class="fas fa-caret-down"></i></span>
            <span v-show="sortColumn2 == 'spend' && sortReverse2"><i class="fas fa-caret-up"></i></span>
            <span v-show="sortColumn2 != 'spend'"><i class="fas fa-caret-up" style="visibility: hidden"></i></span>
          </th>
          <th @click="updateSorting2('frp')" class="sortable rightalign" style="min-width:30%">
            FRP
            <span v-show="sortColumn2 == 'frp' && !sortReverse2"><i class="fas fa-caret-down"></i></span>
            <span v-show="sortColumn2 == 'frp' && sortReverse2"><i class="fas fa-caret-up"></i></span>
            <span v-show="sortColumn2 != 'frp'"><i class="fas fa-caret-up" style="visibility: hidden"></i></span>
          </th>
          <th @click="updateSorting2('equity')" class="sortable rightalign" style="min-width:30%">
            Equity
            <span v-show="sortColumn2 == 'equity' && !sortReverse2"><i class="fas fa-caret-down"></i></span>
            <span v-show="sortColumn2 == 'equity' && sortReverse2"><i class="fas fa-caret-up"></i></span>
            <span v-show="sortColumn2 != 'equity'"><i class="fas fa-caret-up" style="visibility: hidden"></i></span>
          </th>
          <th>
            Actions
          </th>
        </tr>
        </thead>
        <tbody>
        <tr v-for="interv in sortedFilteredIntervs">
          <td style="text-align: center">
            <input type="checkbox"
                   v-model="interv.active"/>
          </td>
          <td>
            <input type="text"
                   class="txbox"
                   @keyup.enter="updateInterv(interv)"
                   v-model="interv.name"/>
          </td>
          <td>
            <input type="text"
                   class="txbox"
                   @keyup.enter="updateInterv(interv)"
                   v-model="interv.platform"/>
          </td>
          <td>
            <input type="text"
                   class="txbox"
                   @keyup.enter="updateInterv(interv)"
                   v-model="interv.burdencov"/>
          </td>
          <td>
            <input type="text"
                   class="txbox rightalign"
                   @keyup.enter="updateInterv(interv)"
                   v-model="interv.icer"/>
          </td>
          <td>
            <input type="text"
                   class="txbox rightalign"
                   @keyup.enter="updateInterv(interv)"
                   v-model="interv.unitcost"/>
          </td>
          <td>
            <input type="text"
                   class="txbox rightalign"
                   @keyup.enter="updateInterv(interv)"
                   v-model="interv.spend"/>
          </td>
          <td>
            <input type="text"
                   class="txbox rightalign"
                   @keyup.enter="updateInterv(interv)"
                   v-model="interv.frp"/>
          </td>
          <td>
            <input type="text"
                   class="txbox rightalign"
                   @keyup.enter="updateInterv(interv)"
                   v-model="interv.equity"/>
          </td>
          <td style="white-space: nowrap">
            <button class="iconbtn" @click="copyInterv(interv)" data-tooltip="Copy intervention"><i class="ti-layers"></i></button>
            <button class="iconbtn" @click="deleteInterv(interv)" data-tooltip="Delete intervention"><i class="ti-trash"></i></button>
          </td>
        </tr>
        </tbody>
      </table>
      <!--<button class="btn" @click="addInterv">Add new intervention</button>--> <!-- Disabled for possible future removal -->
    </div>
  </div>
</template>

<script>
  import axios from 'axios'
  var filesaver = require('file-saver')
  import status from '@/js/status-service'
  import rpcs from '@/js/rpc-service'
  import router from '@/router'

  export default {
    name: 'InterventionsPage',

    data() {
      return {
        filterPlaceholder: 'Type here to filter intervention sets', // Placeholder text for first table filter box
        filterPlaceholder2: 'Type here to filter interventions', // Placeholder text for second table filter box
        filterText: '', // Text in the first table filter box
        filterText2: '', // Text in the second table filter box
        intervSetToRename: null, // What intervention set is being renamed?
        sortColumn: 'updatedTime',  // Column of table used for sorting the intervention sets -- name, creationTime, updatedTime
        sortReverse: false, // Sort in reverse order?
        sortColumn2: 'name',  // Column of table used for sorting the intervention sets -- name, creationTime, updatedTime
        sortReverse2: true, // Sort in reverse order?
        interventionSets: [], // List of objects for intervention sets the project has
        activeIntervSet: {}, // Active intervention set
        interventionList: [],
        country: 'Afghanistan',
        countryList: [
          'Afghanistan',
          'Zimbabwe',
        ]
      }
    },

    computed: {
      activeProjectName() {
        if (this.$store.state.activeProject.project === undefined) {
          return ''
        } else {
          return this.$store.state.activeProject.project.name
        }
      },

      sortedFilteredIntervSets() {
        return this.applyNameFilter(this.applySorting(this.interventionSets))
      },
      
      sortedFilteredIntervs() {
        return this.applyIntervFilter(this.applySorting2(this.interventionList))
      }
    },

    created() {
      if (this.$store.state.currentUser.displayname === undefined) { // If we have no user logged in, automatically redirect to the login page.
        router.push('/login')
      } else { // Otherwise...
        this.updateIntervSets(true) // Load the intervention sets from the active project, telling the function to also set the active intervention set to the last item.
      }
    },

    methods: {

      notImplemented(message) {
        status.fail(this, 'Function "' + message + '" not yet implemented')
      },

      updateIntervSets(setLastEntryActive) {
        console.log('updateIntervSets() called')
        if (this.$store.state.activeProject.project === undefined) { // If there is no active project, clear the interventionSets list.
          this.interventionSets = []
        } else { // Otherwise...
          rpcs.rpc('jsonify_intervsets', [this.$store.state.activeProject.project.id]) // Get the active project's intervention sets.
            .then(response => {
              this.interventionSets = response.data.intervsets // Set the intervention set list to what we received.
              for (let ind=0; ind < this.interventionSets.length; ind++) { // Add numindex elements to the intervention sets to keep track of which index to pull from the server.
                this.interventionSets[ind].intervset.numindex = ind
              }
              this.intervSetToRename = null  // Unset the link to a intervention set being renamed.
              this.interventionSets.forEach(theSet => { // Set renaming values to blank initially.
                theSet.renaming = ''
              })
              if (this.interventionSets.length > 0) { // If we want to set the last entry active and we have any entries, do the setting.
                this.viewSet(this.interventionSets[this.interventionSets.length - 1])
              }
            })
            .catch(error => {
              status.fail(this, 'Could not update interventions set', error)
            })
        }
      },

      intervSetIsSelected(intervSet) {
        if (this.activeIntervSet.intervset === undefined) { // If the active intervention set is undefined, it is not active.
          return false
        } else { // Otherwise, the intervention is selected if the numindexes match.
          return (this.activeIntervSet.intervset.numindex === intervSet.intervset.numindex)
        }
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

      applyNameFilter(sets) {
        console.log(sets)
        return sets.filter(theSet => theSet.intervset.name.toLowerCase().indexOf(this.filterText.toLowerCase()) !== -1)
      },

      applySorting(sets) {
        return sets.sort((set1, set2) =>
          {
            let sortDir = this.sortReverse ? -1: 1
            if      (this.sortColumn === 'name')         {return (set1.intervset.name         > set2.intervset.name         ? sortDir: -sortDir)}
            else if (this.sortColumn === 'creationTime') {return (set1.intervset.creationTime > set2.intervset.creationTime ? sortDir: -sortDir)}
            else if (this.sortColumn === 'updatedTime')  {return (set1.intervset.updateTime   > set2.intervset.updateTime   ? sortDir: -sortDir)}
          }
        )
      },


      updateSorting2(sortColumn) {
        console.log('updateSorting2() called')
        if (this.sortColumn2 === sortColumn) { // If the active sorting column is clicked...
          this.sortReverse2 = !this.sortReverse2 // Reverse the sort.
        } else { // Otherwise.
          this.sortColumn2 = sortColumn // Select the new column for sorting.
          this.sortReverse2 = true // Set the sorting for non-reverse.
        }
      },
      
      applyIntervFilter(intervs) {
        return intervs.filter(theInterv => (theInterv.name.toLowerCase().indexOf(this.filterText2.toLowerCase())      !== -1) ||
                                           (theInterv.platform.toLowerCase().indexOf(this.filterText2.toLowerCase())  !== -1) ||
                                           (theInterv.burdencov.toLowerCase().indexOf(this.filterText2.toLowerCase()) !== -1))
      },
      
      applySorting2(intervs) {
        return intervs.sort((interv1, interv2) =>
          {
            let sortDir = this.sortReverse2 ? -1: 1 // Warning: hard-coded to spreadsheet
            if (this.sortColumn2 === 'name')      { sortDir = -sortDir } // So things sort the way you'd expect
            if (this.sortColumn2 === 'platform')  { sortDir = -sortDir } // So things sort the way you'd expect
            if (this.sortColumn2 === 'burdencov') { sortDir = -sortDir } // So things sort the way you'd expect
            if      (this.sortColumn2 === 'name')     { return (String(interv1[1]).toLowerCase() > String(interv2[1]).toLowerCase() ? sortDir: -sortDir) }
            else if (this.sortColumn2 === 'platform') { return (String(interv1[2]).toLowerCase() > String(interv2[2]).toLowerCase() ? sortDir: -sortDir) }
            else if (this.sortColumn2 === 'burdencov'){ return (String(interv1[3]).toLowerCase() > String(interv2[3]).toLowerCase() ? sortDir: -sortDir) }
            else if (this.sortColumn2 === 'icer')     { return (interv1[4] > interv2[4] ? sortDir: -sortDir) }
            else if (this.sortColumn2 === 'unitcost') { return (interv1[5] > interv2[5] ? sortDir: -sortDir) }
            else if (this.sortColumn2 === 'spend')    { return (interv1[6] > interv2[6] ? sortDir: -sortDir) }
            else if (this.sortColumn2 === 'frp')      { return (interv1[7] > interv2[7] ? sortDir: -sortDir) }
            else if (this.sortColumn2 === 'equity')   { return (interv1[8] > interv2[8] ? sortDir: -sortDir) }
          }
        )
      },

      viewSet(intervSet, verbose) {
        console.log('viewSet() called for ' + intervSet.intervset.name)
        this.activeIntervSet = intervSet // Set the active intervention set to the matched intervention set.
        rpcs.rpc('jsonify_interventions', [this.$store.state.activeProject.project.id, this.activeIntervSet.intervset.numindex]) // Go to the server to get the interventions from the intervention set.
          .then(response => {
            this.interventionList = response.data.interventions // Set the interventions table list.
            for (let ind=0; ind < this.interventionList.length; ind++) { // Set the active values from the loaded in data.
              this.interventionList[ind].numindex = ind
              this.interventionList[ind].active   = (this.interventionList[ind][0] > 0)
              this.interventionList[ind].name     = this.interventionList[ind][1]
              this.interventionList[ind].platform = this.interventionList[ind][2]
              this.interventionList[ind].burdencov= this.interventionList[ind][3]
              this.interventionList[ind].icer     = Number(this.interventionList[ind][4]).toLocaleString()
              this.interventionList[ind].unitcost = Number(this.interventionList[ind][5]).toLocaleString()
              this.interventionList[ind].spend    = Math.round(Number(this.interventionList[ind][6])).toLocaleString()
              this.interventionList[ind].frp      = Number(this.interventionList[ind][7]).toLocaleString()
              this.interventionList[ind].equity   = Number(this.interventionList[ind][8]).toLocaleString()
            }
          })
          .catch(error => {
            status.fail(this, 'Could not view interventions set', error)
          })
        if (verbose) {
          status.succeed(this, 'Intervention set "' + intervSet.intervset.name + '" now active')
        }
      },

      copySet(intervSet) {
        console.log('copySet() called for ' + intervSet.intervset.name)
        rpcs.rpc('copy_set', [this.$store.state.activeProject.project.id, 'interventionset', intervSet.intervset.numindex]) // Have the server copy the intervention set, giving it a new name.
          .then(response => {
            this.updateIntervSets(true) // Update the intervention sets so the new set shows up on the list.
          })
          .catch(error => {
            status.fail(this, 'Could not copy interventions set', error)
          })
      },

      uploadIntervSet(intervSet) {
        console.log('uploadIntervSet() called for ' + intervSet.intervset.name)
        rpcs.upload('upload_set', [this.$store.state.activeProject.project.id, 'interventionset', intervSet.intervset.numindex], {}, '.xlsx')
          .then(response => {
            this.updateIntervSets(true)
            status.succeed(this, 'Intervention set uploaded')
          })
          .catch(error => {
            status.fail(this, 'Could not upload interventions set', error)
          })
      },

      downloadIntervSet(intervSet) {
        console.log('downloadIntervSet() called for ' + intervSet.intervset.name)
        rpcs.download('download_set', [this.$store.state.activeProject.project.id, 'interventionset', intervSet.intervset.numindex])
          .then(response => {
            console.log('Downloaded')
          })
          .catch(error => {
            status.fail(this, 'Could not download interventions set', error)
          })
      },

      finishRename(event) {
        // Grab the element of the open textbox for the intervention set name to be renamed.
        let renameboxElem = document.querySelector('.renamebox')

        // If the click is outside the textbox, renamed the remembered intervention set.
        if (!renameboxElem.contains(event.target)) {
          this.renameSet(this.intervSetToRename)
        }
      },

      renameSet(intervSet) {
        console.log('renameSet() called for ' + intervSet.intervset.name)
        if (intervSet.renaming === '') { // If the intervention set is not in a mode to be renamed, make it so.
          intervSet.renaming = intervSet.intervset.name
          // Add a click listener to run the rename when outside the input box is click, and remember
          // which intervention set needs to be renamed.
          window.addEventListener('click', this.finishRename)
          this.intervSetToRename = intervSet
        } else { // Otherwise (it is to be renamed)...
          // Remove the listener for reading the clicks outside the input box, and null out the intervention set
          // to be renamed.
          window.removeEventListener('click', this.finishRename)
          this.intervSetToRename = null
          rpcs.rpc('rename_set', [this.$store.state.activeProject.project.id, 'interventionset', intervSet.intervset.numindex, intervSet.renaming]) // Have the server change the name of the intervention set.
            .then(response => {
              this.updateIntervSets() // Update the intervention sets so the renamed one shows up on the list.
              intervSet.renaming = '' // Turn off the renaming mode.
            })
            .catch(error => {
              status.fail(this, 'Could not rename interventions set', error)
            })
        }

        // This silly hack is done to make sure that the Vue component gets updated by this function call.
        // Something about resetting the intervention set name informs the Vue component it needs to
        // update, whereas the renaming attribute fails to update it.
        // We should find a better way to do this.
        let theName = intervSet.intervset.name
        intervSet.intervset.name = 'newname'
        intervSet.intervset.name = theName
      },

      deleteSet(intervSet) {
        console.log('deleteSet() called for ' + intervSet.intervset.name)
        rpcs.rpc('delete_set', [this.$store.state.activeProject.project.id, 'interventionset', intervSet.intervset.numindex]) // Go to the server to delete the intervention set.
          .then(response => {
            this.updateIntervSets(true) // Update the intervention sets so the new set shows up on the list.
          })
          .catch(error => {
            status.fail(this, 'Could not delete interventions set', error)
          })
      },

      createNewSet() {
        console.log('createNewSet() called')
        rpcs.rpc('create_intervset', [this.$store.state.activeProject.project.id, this.country]) // Go to the server to create the new intervention set.
          .then(response => {
            this.updateIntervSets(true) // Update the intervention sets so the new set shows up on the list.
          })
          .catch(error => {
            status.fail(this, 'Could not create new interventions set', error)
          })
      },

      updateInterv(interv) {
        console.log('Update to be made')
        console.log('Index: ',     interv.numindex)
        console.log('Active?: ',   interv.active)
        console.log('Name: ',      interv.name)
        console.log('Platform: ',  interv.platform)
        console.log('Burden-cov: ',interv.burdencov)
        console.log('ICER: ',      interv.icer)
        console.log('Unit cost: ', interv.unitcost)
        console.log('FRP: ',       interv.frp)
        console.log('Equity: ',    interv.equity)
        let filterActive = interv.active ? 1 : 0 // Do format filtering to prepare the data to pass to the RPC.
        rpcs.rpc('update_intervention', // Go to the server to update the intervention from the intervention set. Note: filter out commas in the numeric fields.
          [this.$store.state.activeProject.project.id, this.activeIntervSet.intervset.numindex, interv.numindex, // Warning: hard-coded to spreadsheet
            [filterActive, interv.name, interv.platform, interv.burdencov,
              interv.icer.replace(/,/g, ''),
              interv.unitcost.replace(/,/g, ''),
              interv.spend.replace(/,/g, ''),
              interv.frp.replace(/,/g, ''),
              interv.equity.replace(/,/g, '')]])
          .then(response => {
            this.viewSet(this.activeIntervSet) // Update the display of the intervention list by rerunning the active intervention set.
            status.succeed(this, 'Intervention set updated')
          })
          .catch(error => {
            status.fail(this, 'Could not update interventions set', error)
          })
      },

      addInterv() {
        console.log('Adding item')
        rpcs.rpc('add_intervention', [this.$store.state.activeProject.project.id, this.activeIntervSet.intervset.numindex])
          .then(response => {
            this.viewSet(this.activeIntervSet) // Update the display of the intervention list by rerunning the active intervention set.
            status.succeed(this, 'Intervention added')
          })
          .catch(error => {
            status.fail(this, 'Could not add intervention', error)
          })
      },

      copyInterv(interv) {
        console.log('Item to copy:', interv.numindex)
        rpcs.rpc('copy_intervention', [this.$store.state.activeProject.project.id, this.activeIntervSet.intervset.numindex, interv.numindex])
          .then(response => {
            this.viewSet(this.activeIntervSet) // Update the display of the intervention list by rerunning the active intervention set.
            status.succeed(this, 'Intervention copied')
          })
          .catch(error => {
            status.fail(this, 'Could not copy intervention', error)
          })
      },

      deleteInterv(interv) {
        console.log('Item to delete:', interv.numindex)
        rpcs.rpc('delete_intervention', [this.$store.state.activeProject.project.id, this.activeIntervSet.intervset.numindex, interv.numindex])
          .then(response => {
            this.viewSet(this.activeIntervSet) // Update the display of the intervention list by rerunning the active intervention set.
            status.succeed(this, 'Intervention deleted')
          })
          .catch(error => {
            status.fail(this, 'Could not delete intervention', error)
          })
      },
    }
  }
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style lang="scss" scoped>
  #checkboxtable td {
    padding: 0px 5px;
  }
</style>
