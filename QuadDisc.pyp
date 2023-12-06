"""
Copyright: Software Schmid
Author: Daniel Schmid

Description:
    - Creates a disc which consists of quads.

"""

import c4d
import os
import math

from c4d import GeListNode

PLUGIN_ID = 1062048

class Trigonometry:
    @staticmethod
    def CalculateHypotenuse(leg_length):
        # Calculation of the hypotenuse using the Pythagorean theorem
        hypotenuse = math.sqrt(2) * leg_length
        return hypotenuse

    @staticmethod
    def CalculateLegLength(hypotenuse):
        # Calculation of the leg length using the inverse of the Pythagorean theorem
        leg_length = hypotenuse / math.sqrt(2)
        return leg_length

class QuadDiscValues:
    """
    | Provides contextual values of the quad disc object.
    | Values that would otherwise need to be calculated multiple times are stored here.
    | See the Code Helpers in the included scene.
    """

    # User input values
    Radius: float
    Rings: int
    Subdivisions: int
    Orientation: int
    SmoothingIterations: int
    SmoothingStiffness: float
    
    # General values
    RadiusSegments: int
    RadiusSegmentSize: float

    # Ring related values
    RingPointsCount: int
    QuarterRingSegments: int
    RingSegments: int

    # Square related values
    SquareSegments: int
    SquarePointsPerDimension: int
    HalfSquareSize: float

    def __init__(self, op: c4d.BaseObject):
        radius: float = op[c4d.PY_QUADDISC_RADIUS]
        rings: int = op[c4d.PY_QUADDISC_RINGS]
        subdivisions: int = op[c4d.PY_QUADDISC_SUBDIVISIONS]
        orientation: int = op[c4d.PRIM_AXIS] if op[c4d.PRIM_AXIS] is not None else c4d.PRIM_AXIS_YP
        smoothing_iterations: int = op[c4d.PY_QUADDISC_SMOOTHING_ITERATIONS]
        smoothing_stiffness: int = op[c4d.PY_QUADDISC_SMOOTHING_STIFFNESS]

        # General values
        self.Radius = radius
        self.Rings = rings
        self.Subdivisions = subdivisions
        self.Orientation = orientation
        self.SmoothingIterations = smoothing_iterations
        self.SmoothingStiffness = smoothing_stiffness

        self.RadiusSegments = (2 * self.Rings + subdivisions + 1) / 2
        self.RadiusSegmentSize = radius / self.RadiusSegments

        # Ring related values
        self.RingPointsCount = 4 * (subdivisions + 1)
        self.QuarterRingSegments = (subdivisions + 1)
        self.RingSegments = self.QuarterRingSegments * 4

        # Square related values
        self.SquareSegments = subdivisions + 1
        self.SquarePointsPerDimension = self.SquareSegments + 1
        square_size = Trigonometry.CalculateLegLength(self.RadiusSegmentSize * self.SquareSegments / 2.0) * 2.0
        self.HalfSquareSize = square_size / 2.0
        self.square_segment_size = square_size / self.SquareSegments

class Smoothing:
    @staticmethod
    def __getConnectedPoints(poly_obj: c4d.PolygonObject, neighbor: c4d.utils.Neighbor, point_index: int):
        polys_indices = neighbor.GetPointPolys(point_index)

        polys = []

        for poly_index in polys_indices:
            polys.append(poly_obj.GetPolygon(poly_index))

        connected_points = []

        for poly in polys:
            if poly.a == point_index:
                connected_points.append(poly.b)
                if poly.IsTriangle():
                    connected_points.append(poly.c)
                else:
                    connected_points.append(poly.d)

            if poly.b == point_index:
                connected_points.append(poly.a)
                connected_points.append(poly.c)

            if poly.c == point_index:
                connected_points.append(poly.b)

                if poly.IsTriangle():
                    connected_points.append(poly.a)
                else:
                    connected_points.append(poly.d)

            if not poly.IsTriangle() and poly.d == point_index:
                connected_points.append(poly.c)
                connected_points.append(poly.a)

        return connected_points

    @staticmethod
    def SmoothPoints(poly_obj: c4d.PolygonObject, steps: int = 1, stiffness: float = 0.5, points_indices_to_smooth: list[int] = [], neighbor: c4d.utils.Neighbor = None):
        if neighbor is None:
            neighbor = c4d.utils.Neighbor()
            neighbor.Init(poly_obj)

        all_points = poly_obj.GetAllPoints()

        # If no points are defined, smooth all points.
        if not points_indices_to_smooth:
            # Create a list of all point indices.
            points_indices_to_smooth = range(len(all_points))

        for _ in range(steps):
            for point_index in points_indices_to_smooth:
                point = all_points[point_index]

                connected_points_indices = Smoothing.__getConnectedPoints(poly_obj, neighbor, point_index)

                # Calculate center of connected points.
                connected_points = c4d.Vector(0)

                for connected_point_index in connected_points_indices:
                    connected_points += poly_obj.GetPoint(connected_point_index)

                connected_points /= len(connected_points_indices)

                # Apply stiffness.
                new_point = point - (point - connected_points) * (1.0 - stiffness)

                all_points[point_index] = new_point

            for point_index in points_indices_to_smooth:
                poly_obj.SetPoint(point_index, all_points[point_index])

class QuadDisc(c4d.plugins.ObjectData):
    def __init__(self, *args):
        super(QuadDisc, self).__init__(*args)
        self.SetOptimizeCache(True)
    
    def Init(self, op, isCloneInit):
        """Called when Cinema 4D Initialize the ObjectData (used to define, default values).

        Args:
            op: (c4d.GeListNode): The instance of the ObjectData.

        Returns:
            bool: True on success, otherwise False.
        """
        
        self.InitAttr(op, float, c4d.PY_QUADDISC_RADIUS)
        self.InitAttr(op, int, c4d.PY_QUADDISC_RINGS)
        self.InitAttr(op, int, c4d.PY_QUADDISC_SUBDIVISIONS)
        self.InitAttr(op, int, c4d.PY_QUADDISC_SMOOTHING_ITERATIONS)
        self.InitAttr(op, float, c4d.PY_QUADDISC_SMOOTHING_STIFFNESS)
        self.InitAttr(op, int, c4d.PRIM_AXIS)
        
        op[c4d.PY_QUADDISC_RADIUS] = 100.0
        op[c4d.PY_QUADDISC_RINGS] = 2
        op[c4d.PY_QUADDISC_SUBDIVISIONS] = 2
        op[c4d.PY_QUADDISC_SMOOTHING_ITERATIONS] = 5
        op[c4d.PY_QUADDISC_SMOOTHING_STIFFNESS] = 0.0
        op[c4d.PRIM_AXIS] = c4d.PRIM_AXIS_YP

        return True

    def GetVirtualObjects(self, op, hierarchyhelp):
        qd_values = QuadDiscValues(op)

        points: list[c4d.Vector] = []
        polys: list[c4d.CPolygon] = []
        poly_obj: c4d.PolygonObject = c4d.BaseObject(c4d.Opolygon)

        self.__createRings(qd_values, points, polys)
        self.__createSquare(qd_values, points, polys)
        self.__setAxis(qd_values, points)

        self.__fillPolyObj(poly_obj, points, polys)

        self.__smooth(qd_values, poly_obj)

        poly_obj.Message(c4d.MSG_UPDATE)

        phong_tag = op.GetTag(c4d.Tphong)
        if phong_tag is not None:
            phong_tag_clone = phong_tag.GetClone(c4d.COPYFLAGS_NONE)
            poly_obj.InsertTag(phong_tag_clone)
        else:
            poly_obj.SetPhong(True, True, c4d.utils.Rad(80.0))

        return poly_obj

    # Geometry generation
    def __createRings(self, qd_values: QuadDiscValues, points: list[c4d.Vector], polys: list[c4d.CPolygon]):
        onehundredeighty_deg = c4d.utils.DegToRad(180)
        fourtyfive_deg = c4d.utils.DegToRad(45)

        innermost_ring_radius = qd_values.Radius - (qd_values.Rings - 1) * qd_values.RadiusSegmentSize

        for ring_index in range(qd_values.Rings):
            # Create rings from inner to outer.
            ring_radius = innermost_ring_radius + ring_index * qd_values.RadiusSegmentSize
            for point_index in range(qd_values.RingPointsCount):
                angle = (point_index / float(qd_values.RingPointsCount)) * 2.0 * onehundredeighty_deg - fourtyfive_deg
                x,y = c4d.utils.SinCos(angle)
                points.append(c4d.Vector(x * ring_radius, y * ring_radius, 0))

                if ring_index > 0:
                    prev_ring_index = ring_index - 1
                    a = prev_ring_index * qd_values.RingPointsCount + point_index
                    b = ring_index * qd_values.RingPointsCount + point_index
                    c = ring_index * qd_values.RingPointsCount + point_index + 1
                    d = prev_ring_index * qd_values.RingPointsCount + point_index + 1

                    # Wrap the point indices of c and d if this is the last polygon in the ring.
                    is_last_point_of_ring = point_index == qd_values.RingPointsCount - 1
                    if is_last_point_of_ring:
                        c -= qd_values.RingPointsCount
                        d -= qd_values.RingPointsCount

                    poly = c4d.CPolygon(a, b, c, d)
                    polys.append(poly)

    def __createSquare(self, qd_values: QuadDiscValues, points: list[c4d.Vector], polys: list[c4d.CPolygon]):
        first_square_point_index = len(points)
        first_ring_point_index = 0

        # Create the square points.
        for y_i in range(qd_values.SquarePointsPerDimension):
            for x_i in range(qd_values.SquarePointsPerDimension):
                points.append(
                    c4d.Vector(-qd_values.HalfSquareSize + x_i * qd_values.square_segment_size,
                    qd_values.HalfSquareSize - y_i * qd_values.square_segment_size,
                    0))

        # Create the polygons connecting the square to the inner ring.
        for y_i in range(qd_values.SquarePointsPerDimension):
            is_first_row = y_i == 0
            is_last_row = y_i == qd_values.SquarePointsPerDimension - 1

            if is_first_row:
                # Connect first row.
                for x_i in range(qd_values.SquarePointsPerDimension):

                    is_last_column = x_i == qd_values.SquarePointsPerDimension - 1

                    if not is_last_column:
                        polys.append(c4d.CPolygon(
                            first_square_point_index + x_i,
                            x_i,
                            x_i + 1,
                            first_square_point_index + x_i + 1))

            else: # Not first row.
                # Connect left side of square.
                polys.append(c4d.CPolygon(
                    first_square_point_index + y_i * qd_values.SquarePointsPerDimension, # First index of current row.
                    first_ring_point_index + qd_values.RingSegments - y_i,
                    (first_ring_point_index + qd_values.RingSegments - y_i + 1) % qd_values.RingSegments,
                    first_square_point_index + (y_i - 1) * qd_values.SquarePointsPerDimension)) # First index of previous row.

                # Connect right side of square.
                polys.append(c4d.CPolygon(
                    first_square_point_index + y_i * qd_values.SquarePointsPerDimension - 1, # Last index of previous row.
                    first_ring_point_index + qd_values.QuarterRingSegments + y_i - 1,
                    first_ring_point_index + qd_values.QuarterRingSegments + y_i,
                    first_square_point_index + (y_i + 1) * qd_values.SquarePointsPerDimension - 1)) # Last index of current row.

                if is_last_row:
                    # Connect last row.
                    for x_i in reversed(range(qd_values.SquarePointsPerDimension)):
                        is_first_column = x_i == qd_values.SquarePointsPerDimension - 1
                        if is_first_column:
                            continue

                        last_point_index = len(points) - 1
                        first_ring_index = qd_values.QuarterRingSegments * 2

                        polys.append(c4d.CPolygon(
                            last_point_index - x_i,
                            first_ring_index + x_i,
                            first_ring_index + x_i + 1,
                            last_point_index - x_i - 1))

        # Create the other polygons of the square
        for y_i in range(1, qd_values.SquarePointsPerDimension):
            for x_i in range(1, qd_values.SquarePointsPerDimension):
                point_index = first_square_point_index + y_i * qd_values.SquarePointsPerDimension + x_i

                a = point_index - 1
                b = a - qd_values.SquarePointsPerDimension
                c = b + 1
                d = point_index

                polys.append(c4d.CPolygon(a, b, c, d))

    def __fillPolyObj(self, poly_obj: c4d.PolygonObject, points: list[c4d.Vector], polys: list[c4d.CPolygon]):
        poly_obj.ResizeObject(len(points), len(polys))

        for i, point in enumerate(points):
            poly_obj.SetPoint(i, point)

        for i, poly in enumerate(polys):
            poly_obj.SetPolygon(i, poly)

    def __setAxis(self, qd_values: QuadDiscValues, points: list[c4d.Vector]):
        if qd_values.Orientation == c4d.PRIM_AXIS_ZN:
            return

        if qd_values.Orientation == c4d.PRIM_AXIS_ZP:
            for i, point in enumerate(points):
                points[i] = c4d.Vector(-point.x, point.y, point.z)

        elif qd_values.Orientation == c4d.PRIM_AXIS_XP:
            for i, point in enumerate(points):
                points[i] = c4d.Vector(0, point.y, point.x)

        elif qd_values.Orientation == c4d.PRIM_AXIS_XN:
            for i, point in enumerate(points):
                points[i] = c4d.Vector(0, point.y, -point.x)

        elif qd_values.Orientation == c4d.PRIM_AXIS_YP:
            for i, point in enumerate(points):
                points[i] = c4d.Vector(point.x, 0, point.y)

        elif qd_values.Orientation == c4d.PRIM_AXIS_YN:
            for i, point in enumerate(points):
                points[i] = c4d.Vector(point.x, 0, -point.y)

    def __smooth(self, qd_values: QuadDiscValues, poly_obj: c4d.PolygonObject):
        first_square_point_index = qd_values.Rings * qd_values.RingPointsCount

        # Smooth the square vertices
        points_to_smooth = []

        for y_i in range(qd_values.SquarePointsPerDimension):
            for x_i in range(qd_values.SquarePointsPerDimension):
                index_to_select = first_square_point_index + y_i * qd_values.SquarePointsPerDimension + x_i

                points_to_smooth.append(index_to_select)

        Smoothing.SmoothPoints(poly_obj, qd_values.SmoothingIterations, qd_values.SmoothingStiffness, points_to_smooth)

    # /Geometry generation

    def Message(self, node: GeListNode, type: int, data: object) -> bool:
        
        if type == c4d.MSG_MENUPREPARE:
            node.SetPhong(True, True, c4d.utils.DegToRad(40.0))
        
        return True

if __name__ == "__main__":
    # Retrieves the icon path
    directory, _ = os.path.split(__file__)
    fn = os.path.join(directory, "res", "QuadDiscIcon.tiff")

    # Creates a BaseBitmap
    bmp = c4d.bitmaps.BaseBitmap()
    if bmp is None:
        raise MemoryError("Failed to create a BaseBitmap.")

    # Init the BaseBitmap with the icon
    if bmp.InitWith(fn)[0] != c4d.IMAGERESULT_OK:
        raise MemoryError("Failed to initialize the BaseBitmap.")

    # Registers the object plugin
    c4d.plugins.RegisterObjectPlugin(id=PLUGIN_ID,
                                     str="Quad Disc",
                                     g=QuadDisc,
                                     description="quaddisc",
                                     icon=bmp,
                                     info=c4d.OBJECT_GENERATOR)