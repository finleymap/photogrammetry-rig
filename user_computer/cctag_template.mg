{
    "header": {
        "pipelineVersion": "2.2",
        "releaseVersion": "2023.3.0",
        "fileVersion": "1.1",
        "template": true,
        "nodesVersions": {
            "StructureFromMotion": "3.3",
            "ImageMatching": "2.0",
            "FeatureExtraction": "1.3",
            "PrepareDenseScene": "3.1",
            "DepthMapFilter": "4.0",
            "MeshFiltering": "3.0",
            "FeatureMatching": "2.0",
            "CameraInit": "9.0",
            "DepthMap": "5.0",
            "Meshing": "7.0",
            "SfMTransform": "3.1",
            "Texturing": "6.0"
        }
    },
    "graph": {
        "Texturing_1": {
            "nodeType": "Texturing",
            "position": [
                2000,
                0
            ],
            "inputs": {
                "input": "{Meshing_1.output}",
                "imagesFolder": "{DepthMap_1.imagesFolder}",
                "inputMesh": "{MeshFiltering_1.outputMesh}"
            }
        },
        "Meshing_1": {
            "nodeType": "Meshing",
            "position": [
                1600,
                0
            ],
            "inputs": {
                "input": "{DepthMapFilter_1.input}",
                "depthMapsFolder": "{DepthMapFilter_1.output}"
            }
        },
        "DepthMapFilter_1": {
            "nodeType": "DepthMapFilter",
            "position": [
                1400,
                0
            ],
            "inputs": {
                "input": "{DepthMap_1.input}",
                "depthMapsFolder": "{DepthMap_1.output}"
            }
        },
        "ImageMatching_1": {
            "nodeType": "ImageMatching",
            "position": [
                407,
                -55
            ],
            "inputs": {
                "input": "{FeatureExtraction_1.input}",
                "featuresFolders": [
                    "{FeatureExtraction_1.output}"
                ]
            }
        },
        "FeatureExtraction_1": {
            "nodeType": "FeatureExtraction",
            "position": [
                200,
                0
            ],
            "inputs": {
                "input": "{CameraInit_1.output}",
                "describerTypes": [
                    "dspsift",
                    "cctag3"
                ],
                "describerPreset": "high"
            }
        },
        "StructureFromMotion_1": {
            "nodeType": "StructureFromMotion",
            "position": [
                800,
                0
            ],
            "inputs": {
                "input": "{FeatureMatching_1.input}",
                "featuresFolders": "{FeatureMatching_1.featuresFolders}",
                "matchesFolders": [
                    "{FeatureMatching_1.output}",
                    "{FeatureMatching_2.output}"
                ],
                "describerTypes": [
                    "dspsift",
                    "cctag3"
                ]
            }
        },
        "PrepareDenseScene_1": {
            "nodeType": "PrepareDenseScene",
            "position": [
                1000,
                0
            ],
            "inputs": {
                "input": "{SfMTransform_1.output}"
            }
        },
        "CameraInit_1": {
            "nodeType": "CameraInit",
            "position": [
                0,
                0
            ],
            "inputs": {}
        },
        "DepthMap_1": {
            "nodeType": "DepthMap",
            "position": [
                1200,
                0
            ],
            "inputs": {
                "input": "{PrepareDenseScene_1.input}",
                "imagesFolder": "{PrepareDenseScene_1.output}"
            }
        },
        "MeshFiltering_1": {
            "nodeType": "MeshFiltering",
            "position": [
                1800,
                0
            ],
            "inputs": {
                "inputMesh": "{Meshing_1.outputMesh}"
            }
        },
        "FeatureMatching_1": {
            "nodeType": "FeatureMatching",
            "position": [
                602,
                -20
            ],
            "inputs": {
                "input": "{ImageMatching_1.input}",
                "featuresFolders": "{ImageMatching_1.featuresFolders}",
                "imagePairsList": "{ImageMatching_1.output}",
                "minRequired2DMotion": 2.0
            }
        },
        "SfMTransform_1": {
            "nodeType": "SfMTransform",
            "position": [
                914,
                -93
            ],
            "inputs": {
                "input": "{StructureFromMotion_1.output}",
                "method": "from_markers",
                "landmarksDescriberTypes": [
                    "cctag3"
                ],
                "markers": [
                    {
                        "markerId": 1,
                        "markerCoord": {
                            "x": 0.5,
                            "y": 0.0,
                            "z": 0.0
                        }
                    },
                    {
                        "markerId": 2,
                        "markerCoord": {
                            "x": 0.0,
                            "y": 0.0,
                            "z": 0.5
                        }
                    },
                    {
                        "markerId": 3,
                        "markerCoord": {
                            "x": -0.5,
                            "y": 0.0,
                            "z": 0.0
                        }
                    },
                    {
                        "markerId": 4,
                        "markerCoord": {
                            "x": 0.0,
                            "y": 0.0,
                            "z": -0.5
                        }
                    }
                ]
            }
        },
        "FeatureMatching_2": {
            "nodeType": "FeatureMatching",
            "position": [
                602,
                140
            ],
            "inputs": {
                "input": "{ImageMatching_1.input}",
                "featuresFolders": "{ImageMatching_1.featuresFolders}",
                "imagePairsList": "{ImageMatching_1.output}",
                "describerTypes": [
                    "cctag3"
                ],
                "geometricFilterType": "no_filtering"
            }
        }
    }
}