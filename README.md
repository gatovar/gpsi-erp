# **A Template for Documenting Software and Firmware Architectures**
* Michael A. Ogush, Derek Coleman, Dorothea Beringer
* Hewlett-Packard Product Generation Solutions

## **Contact**
* mike_ogush@hp.com
* derek_coleman@hp.com
* dorothea_beringer@hp.com

## **Table of Content**
1. [Table of Content](https://www.google.com)
2. [Overview](https://www.google.com)
3. [Templates for Architectural Documentation](https://www.google.com)
   1. [Introduction Section](https://www.google.com)
   2. [System Purpose Section](https://www.google.com)

## **1. Overview**
In recent years a realization has grown of the importance of software architecture. According to Bass et al
[1], the software architecture of a system is the structure or structures of the system, which comprise
software components, the externally visible properties of those components, and the relationships among
them. The IEEE recommendation [2] defines an architecture as the fundamental organization of a system
embodied in its components, their relationships to each other and to the environment and the principles
guiding its design and evolution. Software architectures are important because they represent the single
abstraction for understanding the structure of a system and form the basis for a shared understanding of a
system and all its stakeholders (product teams, hardware and marketing engineers, senior management, and
external partners).

This paper tackles the problem of how an architecture should be documented. It is a meta-document that
defines a template for producing architectural documentation. As such it defines how to document purpose,
concepts, context and interface of a system, how to specify system structure in terms of components, their
interfaces, and their connections, and how to describe system behavior. Although the paper uses the term
software architecture throughout, the template has proven to be also applicable to firmware architectures
with little or no modification.

The structure and content for an architectural description is given in section three of this paper. Each
subsection of section three describes the form and content of a section of an architecture document. Thus
section 3.1 of this template describes what information should be given in the Introduction section of an
architecture document; section 3.2 describes the Purpose section of an architecture document etc. Most
explanations are accompanied by examples taken from a (fictitious) architecture document for CellKeeper
network management system [3].

A summary of the structure of an architecture document is given in appendix A. Appendix A is the ideal
starting point for everybody who wants to get a quick overview of the various elements of the architecture
template.

Section two of this paper discusses the different contents, purposes and readerships for architectural
documentation and how that affects the use of the template. Appendix B shows how the architecture
template presented here relates to the IEEE Draft Recommended Practice for Architectural Description.
Appendix C contains a glossary of important terms.

## **2. The Role and Content of Architectural Documentation**
Architectural overview and architectural reference manual
The template can be used to produce two different kinds of architectural documentation, an architectural
overview and an architectural reference manual.

An architectural overview is aimed at providing a shared understanding of the architecture across a broad
range of people including the developers, marketing, management and possibly potential end-users. An
architectural overview is ideally produced early in the development lifecycle and serves as the starting
point for the development. An architectural overview should be at a high level of abstraction. All the major
functionalities and components of the architecture should be described but the descriptions may lack detail
and precision as they often use natural language rather than formal notations.

An architectural reference manual describes an architecture in a detailed and precise manner. Unlike an
architectural overview, an architectural reference manual is not written at one particular point in time.
Rather a reference manual should be a living document that is constructed collaboratively by the
development team as the development proceeds. As it develops the reference manual can be used to track
progress of the software development and for assessing the impact of proposed requirements changes.
When complete the reference manual is the basis for system maintenance and enhancements. The reference
manual should be updated as changes occur so it always reflects the actual architecture.

A reference manual needs to be complete in the sense that every facet of the architecture should be
documented. Although a reference manual will tend to be detailed and technical in nature the level of
abstraction and precision is likely to vary across the architecture and across different projects. The
architecture within very large grained components should be documented in separate architectural reference
manuals for the components. The level of completeness, formality, detail and precision used for any
particular aspect of the architecture will depend on the associated technical or business risk.

### *Scoping*
Not every architecture documentation requires all the sections described in this template. Appendix A gives
a summary of all the sections and shows which ones are optional. Yet even for the mandatory sections the
amount of information documented not only varies between architectural overview and architectural
reference manual, but also from project to project. The introduction section of the architecture document
lists the stakeholders and their concerns. An architecture document is complete as soon as the concerns of
the stakeholders are met.

### *Views covered by the architecture template*
The template has been structured according to the 4 views of the 4+1 view model of Kruchten [4]: the
logical view is modeled in the structure section and the dynamic behavior section, the process view, the
physical view and the development view are modeled in the other views section.

For each view the structure of the components and the dynamic behavior, i.e. scenarios showing the
interactions of the components, are modeled. For the process, physical and development view this is done
in the process, physical, or development view sections. For the logical view, it is split up into two sections:
the structure section and the dynamic behavior section. Of course, the dynamic models in the different
views must be consistent. They can be looked at as the integrating force between the various views.