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
import router from '../router.js'
import sciris from 'sciris-js';

export default {
  name: 'InterventionsPage',

  data() {
    return {
      // Placeholder text for first table filter box
      filterPlaceholder: 'Type here to filter intervention sets',

      // Placeholder text for second table filter box
      filterPlaceholder2: 'Type here to filter interventions',

      // Text in the first table filter box
      filterText: '',

      // Text in the second table filter box
      filterText2: '', 

      // What intervention set is being renamed?
      intervSetToRename: null,

      // Column of table used for sorting the intervention sets
      // Option: name, creationTime, updatedTime
      sortColumn: 'updatedTime',

      // Sort in reverse order?
      sortReverse: false,

      // Column of table used for sorting the intervention sets
      // Options: name, creationTime, updatedTime
      sortColumn2: 'name',

      // Sort in reverse order?
      sortReverse2: true, 

      // List of objects for intervention sets the project has
      interventionSets: [],

      // Active intervention set
      activeIntervSet: {},
      interventionList: [],
      country: 'Demo',
      countryList: [
        'Demo',
        // 'Afghanistan',
        // 'Zimbabwe',
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
    // If we have no user logged in, automatically redirect to the login page.
    if (this.$store.state.currentUser.displayname === undefined) {
      router.push('/login')
    } else {
      // Load the intervention sets from the active project, telling 
      // the function to also set the active intervention set to the last item.
      this.updateIntervSets(true) 
    }
  },

  methods: {

    notImplemented(message) {
      sciris.fail(this, 'Function "' + message + '" not yet implemented')
    },

    updateIntervSets(setLastEntryActive) {
      console.log('updateIntervSets() called')
      // If there is no active project, clear the interventionSets list.
      if (this.$store.state.activeProject.project === undefined) { 
        this.interventionSets = []
      } else {
        // Get the active project's intervention sets.
        sciris.rpc('jsonify_intervsets', [
          this.$store.state.activeProject.project.id
        ]) 
        .then(response => {
          // Set the intervention set list to what we received.
          this.interventionSets = response.data.intervsets

          // Add numindex elements to the intervention sets to keep 
          // track of which index to pull from the server.
          for (let ind=0; ind < this.interventionSets.length; ind++) {
            this.interventionSets[ind].intervset.numindex = ind
          }

          // Unset the link to a intervention set being renamed.
          this.intervSetToRename = null

          // Set renaming values to blank initially.
          this.interventionSets.forEach(theSet => {
            theSet.renaming = ''
          })

          // If we want to set the last entry active and we have any entries, do the setting.
          if (this.interventionSets.length > 0) {
            this.viewSet(this.interventionSets[this.interventionSets.length - 1])
          }
        })
        .catch(error => {
          sciris.fail(this, 'Could not update interventions set', error)
        })
      }
    },

    intervSetIsSelected(intervSet) {
      // If the active intervention set is undefined, it is not active.
      if (this.activeIntervSet.intervset === undefined) {
        return false
      } else {
        // Otherwise, the intervention is selected if the numindexes match.
        return (this.activeIntervSet.intervset.numindex === intervSet.intervset.numindex)
      }
    },

    updateSorting(sortColumn) {
      console.log('updateSorting() called')

      // If the active sorting column is clicked...
      if (this.sortColumn === sortColumn) {

        // Reverse the sort.
        this.sortReverse = !this.sortReverse 

      } else { 

        // Select the new column for sorting.
        this.sortColumn = sortColumn

        // Set the sorting for non-reverse.
        this.sortReverse = false

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
      // If the active sorting column is clicked...
      if (this.sortColumn2 === sortColumn) {
        // Reverse the sort.
        this.sortReverse2 = !this.sortReverse2
      } else {
        // Select the new column for sorting.
        this.sortColumn2 = sortColumn

        // Set the sorting for non-reverse.
        this.sortReverse2 = true
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

      // Set the active intervention set to the matched intervention set.
      this.activeIntervSet = intervSet 


      // Go to the server to get the interventions from the intervention set.
      sciris.rpc('jsonify_interventions', [
        this.$store.state.activeProject.project.id, 
        this.activeIntervSet.intervset.numindex
      ])
      .then(response => {
        // Set the interventions table list.
        this.interventionList = response.data.interventions

        // Set the active values from the loaded in data.
        for (let ind=0; ind < this.interventionList.length; ind++) {
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
        sciris.fail(this, 'Could not view interventions set', error)
      })
      if (verbose) {
        sciris.succeed(this, 'Intervention set "' + intervSet.intervset.name + '" now active')
      }
    },

    copySet(intervSet) {
      console.log('copySet() called for ' + intervSet.intervset.name)
      // Have the server copy the intervention set, giving it a new name.
      sciris.rpc('copy_set', [
        this.$store.state.activeProject.project.id, 
        'interventionset', 
        intervSet.intervset.numindex
      ]) 
      .then(response => {
        // Update the intervention sets so the new set shows up on the list.
        this.updateIntervSets(true)
      })
      .catch(error => {
        sciris.fail(this, 'Could not copy interventions set', error)
      })
    },

    uploadIntervSet(intervSet) {
      console.log('uploadIntervSet() called for ' + intervSet.intervset.name)
      sciris.upload(
        'upload_set', [
          this.$store.state.activeProject.project.id, 
          'interventionset', 
          intervSet.intervset.numindex
        ], {}, '.xlsx')
        .then(response => {
          this.updateIntervSets(true)
          sciris.succeed(this, 'Intervention set uploaded')
        })
        .catch(error => {
          sciris.fail(this, 'Could not upload interventions set', error)
        })
    },

    downloadIntervSet(intervSet) {
      console.log('downloadIntervSet() called for ' + intervSet.intervset.name)
      sciris.download('download_set', [
        this.$store.state.activeProject.project.id, 
        'interventionset', 
        intervSet.intervset.numindex
      ])
      .then(response => {
        console.log('Downloaded')
      })
      .catch(error => {
        sciris.fail(this, 'Could not download interventions set', error)
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
        // Have the server change the name of the intervention set.
        sciris.rpc('rename_set', [
          this.$store.state.activeProject.project.id, 
          'interventionset', 
          intervSet.intervset.numindex, 
          intervSet.renaming
        ]) 
        .then(response => {
          // Update the intervention sets so the renamed one shows up on the list.
          this.updateIntervSets() 
          // Turn off the renaming mode.
          intervSet.renaming = ''
        })
        .catch(error => {
          sciris.fail(this, 'Could not rename interventions set', error)
        })
      }

      /**
        This silly hack is done to make sure that the Vue component gets updated 
        by this function call. Something about resetting the intervention set 
        name informs the Vue component it needs to update, whereas the renaming 
        attribute fails to update it. We should find a better way to do this.
      **/
      let theName = intervSet.intervset.name
      intervSet.intervset.name = 'newname'
      intervSet.intervset.name = theName
    },

    deleteSet(intervSet) {
      console.log('deleteSet() called for ' + intervSet.intervset.name)
      // Go to the server to delete the intervention set.
      sciris.rpc('delete_set', [
        this.$store.state.activeProject.project.id, 
        'interventionset', 
        intervSet.intervset.numindex
      ])
      .then(response => {
        // Update the intervention sets so the new set shows up on the list.
        this.updateIntervSets(true) 
      })
      .catch(error => {
        sciris.fail(this, 'Could not delete interventions set', error)
      })
    },

    createNewSet() {
      console.log('createNewSet() called')
      // Go to the server to create the new intervention set.
      sciris.rpc('create_intervset', [
        this.$store.state.activeProject.project.id, 
        this.country
      ])
      .then(response => {
        // Update the intervention sets so the new set shows up on the list.
        this.updateIntervSets(true)
      })
      .catch(error => {
        sciris.fail(this, 'Could not create new interventions set', error)
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

      // Do format filtering to prepare the data to pass to the RPC.
      let filterActive = interv.active ? 1 : 0 

      // Go to the server to update the intervention from the intervention set. 
      // Note: filter out commas in the numeric fields.
      sciris.rpc('update_intervention', [
        this.$store.state.activeProject.project.id, 
        this.activeIntervSet.intervset.numindex, 
        interv.numindex, // Warning: hard-coded to spreadsheet
        [
          filterActive, 
          interv.name, 
          interv.platform, 
          interv.burdencov,
          interv.icer.replace(/,/g, ''),
          interv.unitcost.replace(/,/g, ''),
          interv.spend.replace(/,/g, ''),
          interv.frp.replace(/,/g, ''),
          interv.equity.replace(/,/g, '')
        ]
      ])
      .then(response => {
        // Update the display of the intervention list by rerunning 
        // the active intervention set.
        this.viewSet(this.activeIntervSet) 
        sciris.succeed(this, 'Intervention set updated')
      })
      .catch(error => {
        sciris.fail(this, 'Could not update interventions set', error)
      })
    },

    addInterv() {
      console.log('Adding item')
      sciris.rpc('add_intervention', [
        this.$store.state.activeProject.project.id, 
        this.activeIntervSet.intervset.numindex
      ])
      .then(response => {
        // Update the display of the intervention list 
        // by rerunning the active intervention set.
        this.viewSet(this.activeIntervSet)
        sciris.succeed(this, 'Intervention added')
      })
      .catch(error => {
        sciris.fail(this, 'Could not add intervention', error)
      })
    },

    copyInterv(interv) {
      console.log('Item to copy:', interv.numindex)
      sciris.rpc('copy_intervention', [
        this.$store.state.activeProject.project.id, 
        this.activeIntervSet.intervset.numindex, 
        interv.numindex
      ])
      .then(response => {
        // Update the display of the intervention list 
        // by rerunning the active intervention set.
        this.viewSet(this.activeIntervSet)
        sciris.succeed(this, 'Intervention copied')
      })
      .catch(error => {
        sciris.fail(this, 'Could not copy intervention', error)
      })
    },

    deleteInterv(interv) {
      console.log('Item to delete:', interv.numindex)
      sciris.rpc('delete_intervention', [
        this.$store.state.activeProject.project.id, 
        this.activeIntervSet.intervset.numindex, 
        interv.numindex
      ])
      .then(response => {
        // Update the display of the intervention list by rerunning 
        // the active intervention set.
        this.viewSet(this.activeIntervSet)
        sciris.succeed(this, 'Intervention deleted')
      })
      .catch(error => {
        sciris.fail(this, 'Could not delete intervention', error)
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
