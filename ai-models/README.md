# AI Models Integration Plan

This MVP ships with a contour-based fallback detector. Production roadmap:

1. Use YOLOv8 for garment class + part proposal bounding boxes.
2. Use Segment Anything Model to segment each proposed part mask.
3. Post-process with OpenCV contour simplification + smoothing for CAD vectors.
4. Feed polygon outlines to `pattern-engine` for reconstruction and grading.
