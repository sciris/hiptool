/**
 * Utilities that are shared across pages
 */

import rpcs from '@/services/rpc-service'
import status from '@/services/status-service'

function sleep(time) {
  // Return a promise that resolves after _time_ milliseconds.
  return new Promise((resolve) => setTimeout(resolve, time));
}

function getUniqueName(fileName, otherNames) {
  let tryName = fileName
  let numAdded = 0
  while (otherNames.indexOf(tryName) > -1) {
    numAdded = numAdded + 1
    tryName = fileName + ' (' + numAdded + ')'
  }
  return tryName
}

function updateSorting(vm, sortColumn) {
  console.log('updateSorting() called')
  if (vm.sortColumn === sortColumn) { // If the active sorting column is clicked...
    vm.sortReverse = !vm.sortReverse // Reverse the sort.
  } else { // Otherwise.
    vm.sortColumn = sortColumn // Select the new column for sorting.
    vm.sortReverse = false // Set the sorting for non-reverse.
  }
}

function projectID(vm) {
  if (vm.$store.state.activeProject.project === undefined) {
    return ''
  } else {
    let projectID = vm.$store.state.activeProject.project.id
    return projectID
  }
}

function hasData(vm) {
  if (vm.$store.state.activeProject.project === undefined) {
    return false
  }
  else {
    return vm.$store.state.activeProject.project.hasData
  }
}


function exportGraphs(vm, project_id) {
  console.log('exportGraphs() called')
  rpcs.download('export_graphs', [project_id]) // Make the server call to download the framework to a .prj file.
    .catch(error => {
      status.failurePopup(vm, 'Could not download graphs: ' + error.message)
    })
}

function exportResults(vm, project_id) {
  console.log('exportResults()')
  rpcs.download('export_results', [project_id]) // Make the server call to download the framework to a .prj file.
    .catch(error => {
      status.failurePopup(vm, 'Could not export results: ' + error.message)
    })
}


//
// Graphs DOM functions
//

function showBrowserWindowSize() {
  var w = window.innerWidth;
  var h = window.innerHeight;
  var ow = window.outerWidth; //including toolbars and status bar etc.
  var oh = window.outerHeight;
  console.log('Browser window size:')
  console.log('Inner width: ', w)
  console.log('Inner height: ', h)
  console.log('Outer width: ', ow)
  console.log('Outer height: ', oh)
  window.alert('Browser window size:\n'+
    'Inner width: ' + w + '\n' +
    'Inner height: ' + h + '\n' +
    'Outer width: ' + ow + '\n' +
    'Outer height: ' + oh + '\n')
}

function scaleElem(svg, frac) {
  // It might ultimately be better to redraw the graph, but this works
  var width  = svg.getAttribute("width")
  var height = svg.getAttribute("height")
  var viewBox = svg.getAttribute("viewBox")
  if (!viewBox) {
    svg.setAttribute("viewBox",  '0 0 ' + width + ' ' + height)
  }
  // if this causes the image to look weird, you may want to look at "preserveAspectRatio" attribute
  svg.setAttribute("width",  width*frac)
  svg.setAttribute("height", height*frac)
}

function scaleFigs(frac) {
  var graphs = window.top.document.querySelectorAll('svg.mpld3-figure')
  for (var g = 0; g < graphs.length; g++) {
    scaleElem(graphs[g], frac)
  }
}

export default {
  sleep,
  getUniqueName,
  updateSorting,
  projectID,
  hasData,
  exportGraphs,
  exportResults,
  scaleFigs,
  showBrowserWindowSize,
}