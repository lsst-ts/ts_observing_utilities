.. _version_history:Version_History:

===============
Version History
===============

.. At the time of writing the Version history/release notes are not yet standardized amongst CSCs.
.. Until then, it is not expected that both a version history and a release_notes be maintained.
.. It is expected that each CSC link to whatever method of tracking is being used for that CSC until standardization occurs.
.. No new work should be required in order to complete this section.
.. Below is an example of a version history format.

v0.4.3
------

* In ``auxtel/latiss/getters``:

  * Add synchronous version of ``get_image`` to be used in synchronous applications.
  * Remove inline logger and pass an optional logger to ``get_image``.
    If no logger is provided, one is created to log information.
  * Update ``get_image`` to add type annotations and pass in ``detector`` to ``getExposure``.
* Reformat with latest version of black.
* Modernize conda recipe.
* Modernize package setup.
* Add Jenkinsfile for CI.
* Update package to use new pre-commit-config.

v0.4.2
------
* Change archiver reference to oods one due to image creation process change (DMTN-143)

v0.4.1
------
* Added Jenkinsfile for conda recipe
* Added conda recipe
* Incorporated new offset parameters with the option of them being persistent (sticky)
